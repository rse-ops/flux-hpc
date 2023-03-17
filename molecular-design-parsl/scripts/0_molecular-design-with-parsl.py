#!/usr/bin/env python3
# coding: utf-8

import argparse
import os


from matplotlib import pyplot as plt
from chemfunctions import compute_vertical
from concurrent.futures import as_completed
from tqdm.notebook import tqdm
from parsl.executors import FluxExecutor
from parsl.app.python import PythonApp
from parsl.app.app import python_app
from parsl.config import Config
from time import monotonic
from random import sample
import pandas as pd
import numpy as np
import parsl
import os
import sys

here = os.path.abspath(os.path.dirname(__name__))
sys.path.insert(0, here)

parser = argparse.ArgumentParser()

parser.add_argument(
    "--workers",
    type=int,
    help="Number of workers (defaults to cpu count)",
    default=os.cpu_count(),
)
parser.add_argument(
    "--outdir",
    help="Output directory (defaults PWD if not defined)",
    default=os.getcwd(),
)
parser.add_argument(
    "--working-dir",
    help="Working directory for Flux (defaults to PWD)",
    default=os.getcwd(),
)
parser.add_argument(
    "--search-space",
    help="search space of molecules (selected randomly from the QM9 database)",
    default="data/QM9-search.tsv",
)
parser.add_argument(
    "--initial-count",
    type=int,
    help="Number of calculations to run at first",
    default=8,
)
parser.add_argument(
    "--search-count",
    type=int,
    help="Number of molecules to evaluate in total",
    default=64,
)
parser.add_argument(
    "--batch-size",
    type=int,
    help="Number of molecules to evaluate in each batch of simulations",
    default=4,
)
parser.add_argument(
    "--flux-workers", type=int, help="Number of flux node available to run", default=4
)

args = parser.parse_args()


# Our search space of molecules
n_workers = min(4, args.workers)
search_space = pd.read_csv(args.search_space, delim_whitespace=True)

# Number of calculations to run at first
initial_count: int = args.initial_count

# Number of molecules to evaluate in total
search_count: int = args.search_count

# Number of molecules to evaluate in each batch of simulations
batch_size: int = args.batch_size


# Set up Parsl to use Flux
# https://parsl.readthedocs.io/en/stable/userguide/configuring.html

executor = FluxExecutor(working_dir=args.working_dir)

# Workaround for bug that it isn't set if provided
executor.launch_cmd="{flux} submit {python} {manager} {protocol} {hostname} {port}"
config = Config(executors=[executor])
parsl.load(config)

# ## Make an initial dataset
# This selects a set of molecules at random from our search space,
#   performs some simulations on those molecules
#   trains on the results.

# ### Execute a first simulation
# We need to prepare this function to run with Parsl. All we need to do is wrap this function with Parsl's `python_app`:
compute_vertical_app = python_app(compute_vertical)
compute_vertical_app

#  Run water as a demonstration (O is the SMILES for water)
future = compute_vertical_app("O")


# This blocks
ie = future.result()
print(f"The ionization energy of {future.task_def['args'][0]} is {ie:.2f} Ha")


# ### Scale the simulation
#
# Scale our simulation and run it for several different molecules and gather their results.
# Use a loop to generate more futures, run computations in the background

smiles = search_space.sample(initial_count)["smiles"]
futures = [compute_vertical_app(s) for s in smiles]
print(f"Submitted {len(futures)} calculations to start with")


# Training

train_data = []
while len(futures) > 0:
    # First, get the next completed computation from the list
    future = next(as_completed(futures))

    # Remove it from the list of still-running tasks
    futures.remove(future)

    # Get the input
    smiles = future.task_def["args"][0]

    # Check if the run completed successfully
    if future.exception() is not None:
        # If it failed, pick a new SMILES string at random and submit it
        print(f"Computation for {smiles} failed, submitting a replacement computation")
        smiles = search_space.sample(1).iloc[0]["smiles"]  # pick one molecule
        new_future = compute_vertical_app(smiles)  # launch a simulation in Parsl
        futures.append(new_future)  # store the Future so we can keep track of it
    else:
        # If it succeeded, store the result
        print(f"Computation for {smiles} succeeded")
        train_data.append(
            {"smiles": smiles, "ie": future.result(), "batch": 0, "time": monotonic()}
        )


# Load initial set of training data into a DataFrame
# This has randomly sampled molecules alongside the simulated ionization energy "ie"
train_data = pd.DataFrame(train_data)
train_data


# Train a machine learning model to screen candidate molecules
@python_app
def train_model(train_data):
    """Train a machine learning model using Morgan Fingerprints.

    Args:
        train_data: Dataframe with a 'smiles' and 'ie' column
            that contains molecule structure and property, respectfully.
    Returns:
        A trained model
    """
    # Imports for python functions run remotely must be defined inside the function
    from chemfunctions import MorganFingerprintTransformer
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.pipeline import Pipeline

    model = Pipeline(
        [
            ("fingerprint", MorganFingerprintTransformer()),
            (
                "knn",
                KNeighborsRegressor(
                    n_neighbors=4, weights="distance", metric="jaccard", n_jobs=-1
                ),
            ),  # n_jobs = -1 lets the model run all available processors
        ]
    )

    return model.fit(train_data["smiles"], train_data["ie"])


# Execute the function and run it asynchronously with Parsl
train_future = train_model(train_data)


@python_app
def run_model(model, smiles):
    """Run a model on a list of smiles strings

    Args:
        model: Trained model that takes SMILES strings as inputs
        smiles: List of molecules to evaluate
    Returns:
        A dataframe with the molecules and their predicted outputs
    """
    import pandas as pd

    pred_y = model.predict(smiles)
    return pd.DataFrame({"smiles": smiles, "ie": pred_y})


@python_app
def combine_inferences(inputs=[]):
    """Concatenate a series of inferences into a single DataFrame
    Args:
        inputs: a list of the component DataFrames
    Returns:
        A single DataFrame containing the same inferences
    """
    import pandas as pd

    return pd.concat(inputs, ignore_index=True)


# Chop up the search space into chunks, and invoke `run_model`  once for each chunk

# Chunk the search space into smaller pieces, so that each can run in parallel
chunks = np.array_split(search_space["smiles"], 64)
inference_futures = [run_model(train_future, chunk) for chunk in chunks]

# Prepare to combine results into a single DataFrame using `combine_inferences`
#  See: https://parsl.readthedocs.io/en/stable/userguide/workflow.html#mapreduce
predictions = combine_inferences(inputs=inference_futures).result()


# Get results - predicted IE values for all molecules in our search space. We can print out the best five molecules, according to the trained model:

predictions.sort_values("ie", ascending=False).head(5)

# Make the search space a list so that we can remove completed molecules more easily
with tqdm(total=search_count) as prog_bar:  # setup a graphical progress bar
    # Mark when we started
    start_time = monotonic()

    # Submit with some random guesses
    train_data = []
    init_mols = search_space.sample(initial_count)["smiles"]
    sim_futures = [compute_vertical_app(mol) for mol in init_mols]
    already_ran = set()

    # Loop until you finish populating the initial set
    while len(sim_futures) > 0:
        # First, get the next completed computation from the list
        future = next(as_completed(sim_futures))

        # Remove it from the list of still-running tasks
        sim_futures.remove(future)

        # Get the input
        smiles = future.task_def["args"][0]
        already_ran.add(smiles)

        # Check if the run completed successfully
        if future.exception() is not None:
            # If it failed, pick a new SMILES string at random and submit it
            smiles = search_space.sample(1).iloc[0]["smiles"]  # pick one molecule
            new_future = compute_vertical_app(smiles)  # launch a simulation in Parsl
            sim_futures.append(
                new_future
            )  # store the Future so we can keep track of it
        else:
            # If it succeeded, store the result
            prog_bar.update(1)
            train_data.append(
                {
                    "smiles": smiles,
                    "ie": future.result(),
                    "batch": 0,
                    "time": monotonic() - start_time,
                }
            )

    # Create the initial training set as a
    train_data = pd.DataFrame(train_data)

    # Loop until complete
    batch = 1
    while len(train_data) < search_count:
        # Train and predict as show in the previous section.
        train_future = train_model(train_data)
        inference_futures = [
            run_model(train_future, chunk)
            for chunk in np.array_split(search_space["smiles"], 64)
        ]
        predictions = combine_inferences(inputs=inference_futures).result()

        # Sort the predictions in descending order, and submit new molecules from them
        predictions.sort_values("ie", ascending=False, inplace=True)
        sim_futures = []
        for smiles in predictions["smiles"]:
            if smiles not in already_ran:
                sim_futures.append(compute_vertical_app(smiles))
                already_ran.add(smiles)
                if len(sim_futures) >= batch_size:
                    break

        # Wait for every task in the current batch to complete, and store successful results
        new_results = []
        for future in as_completed(sim_futures):
            if future.exception() is None:
                prog_bar.update(1)
                new_results.append(
                    {
                        "smiles": future.task_def["args"][0],
                        "ie": future.result(),
                        "batch": batch,
                        "time": monotonic() - start_time,
                    }
                )

        # Update the training data and repeat
        batch += 1
        train_data = pd.concat(
            (train_data, pd.DataFrame(new_results)), ignore_index=True
        )


# Plot the training data against the time of simulation, showing that the model is finding better molecules over time.

fig, ax = plt.subplots(figsize=(4.5, 3.0))
ax.scatter(train_data["time"], train_data["ie"])
ax.step(train_data["time"], train_data["ie"].cummax(), "k--")
ax.set_xlabel("Walltime (s)")
ax.set_ylabel("Ion. Energy (Ha)")
fig.tight_layout()

# Save that data for comparison with another application later
plt.savefig(os.path.join(args.outdir, "training-data-vs-time.svg"))
train_data.to_csv(os.path.join(args.outdir, "parsl-results.csv"), index=False)

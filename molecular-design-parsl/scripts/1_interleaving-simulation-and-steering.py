#!/usr/bin/env python
# coding: utf-8

from matplotlib import pyplot as plt
from ipywidgets import widgets
from colmena.models import Result
from colmena.task_server.parsl import ParslTaskServer
from colmena.queue.python import PipeQueues
from colmena.thinker.resources import ResourceCounter
from colmena.thinker import (
    BaseThinker,
    event_responder,
    task_submitter,
    result_processor,
)
from parsl.executors import FluxExecutor
from parsl.config import Config
from random import shuffle
from time import perf_counter
from threading import Lock, Event
from typing import List
from chemfunctions import compute_vertical, train_model, run_model
from tqdm.notebook import tqdm
import pandas as pd
import numpy as np
import logging
import argparse
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
    "--hostname", help="Hostname for task columna server", default="localhost"
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
    "--flux-workers", type=int, help="Number of flux node available to run", default=4
)


args = parser.parse_args()


n_workers = min(4, args.workers)


handlers = [logging.FileHandler("colmena.log", mode="w")]
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=handlers,
)

search_space = pd.read_csv(
    args.search_space, delim_whitespace=True
)  # Our search space of molecules
initial_count: int = args.initial_count
search_count: int = args.search_count
batch_size: int = args.batch_size

# ## Building a Colmena Application
# Colmena applications have a _Task Server_ to manages execution of computations at the direction of a _Thinker_ through a _Task Queue_.

# ### Creating Task Queue
# A task queue is responsible for conveying requests to perform a computation to a Task Server, and then supplying results back to the Thinker.
# Creating a task queue requires defining connection information to Redis and the names of separate topics used to separate different kinds of tasks
queues = PipeQueues(
    topics=["simulate", "train", "infer"], serialization_method="pickle"
)

# ### Defining Task Server
# The Task Server requires:
#   a task queue to communicate through
#   a list of methods
#   a set of computational resources to run them on. (See [Colmena Docs](https://colmena.readthedocs.io/en/latest/how-to.html#configuring-a-task-server))
#

# Set up Parsl to use Flux
# https://parsl.readthedocs.io/en/stable/userguide/configuring.html

executor = FluxExecutor(working_dir=args.working_dir)

# Workaround for bug that it isn't set if provided
executor.launch_cmd="{flux} submit {python} {manager} {protocol} {hostname} {port}"
config = Config(executors=[executor])

# This will run in the background and will need a kill signal
task_server = ParslTaskServer(
    methods=[compute_vertical, train_model, run_model],
    queues=queues,
    config=config,
)
task_server.start()

queues.send_inputs("C", method="compute_vertical")
result = queues.get_result()
queues.send_inputs("C", method="compute_vertical", topic="simulate")

# Show that we do not pull results on other topics
try:
    result = queues.get_result(topic="infer", timeout=15)
except:
    print("Timed out, as expected.")

# Pull from the correct queue
result = queues.get_result(topic="simulate")


# ## Building a Thinker
# The Thinker part of a Colmena application coordinates what tasks are run by the Task Server.

# Colmena provides [many kinds of decorators for common types of agents](https://colmena.readthedocs.io/en/latest/thinker.html#special-purpose-agents).
# In this demo, we use three of them:
#
# - `task_submitter` runs when resources are available.
# - `result_processor` runs when a certain topic of task completes
# - `event_responder` runs when an [`Event`](https://docs.python.org/3/library/threading.html#event-objects) is set
#
# A simple example for a Thinker is one that submits a new calculation from a list when another completes.


class RandomThinker(BaseThinker):
    """A thinker which evaluates molecules in a random order."""

    def __init__(
        self, queues, n_to_evaluate: int, n_parallel: int, molecule_list: List[str]
    ):
        """Initialize the thinker

        Args:
            queues: Client side of queues
            n_to_evaluate: Number of molecules to evaluate
            n_parallel: Number of computations to run in parallel
            molecule_list: List of SMILES strings
        """
        super().__init__(
            queues,
            # Establishes pools of resources for each kind of task
            #  We'll only use the "simulation" pool
            ResourceCounter(n_parallel, ["simulate", "train", "infer"]),
        )

        # Store the user settings
        self.molecule_list = set(molecule_list)
        self.n_to_evaluate = n_to_evaluate

        # Create a database of evaluated molecules
        self.database = dict()

        # Create a record of completed calculations
        self.simulation_results = []

        # Create a priority list of molecules, starting with them ordered randomly
        self.priority_list = list(self.molecule_list)
        shuffle(self.priority_list)
        self.priority_list_lock = Lock()  # Ensures two agents cannot use it

        # Create a tracker for how many sent and how many complete
        self.rec_progbar = tqdm(total=n_to_evaluate, desc="started")
        self.sent_progbar = tqdm(total=n_to_evaluate, desc="successful")

        # Assign all of the resources over to simulation
        self.rec.reallocate(None, "simulate", n_parallel)

    @task_submitter(task_type="simulate", n_slots=1)
    def submit_calc(self):
        """Submit a calculation when resources are available"""

        with self.priority_list_lock:
            next_mol = self.priority_list.pop()  # Get the next best molecule

        # Send it to the task server to run
        self.queues.send_inputs(next_mol, method="compute_vertical")
        self.rec_progbar.update(1)

    @result_processor
    def receive_calc(self, result: Result):
        """Store the output of a run if it is successful"""

        # Mark that the resources are now free
        self.rec.release("simulate", 1)

        # Store the result if successful
        if result.success:
            # Store the result in a database
            self.database[result.args[0]] = result.value

            # Mark that we've received a result
            self.sent_progbar.update(1)

            # If we've got all of the simulations complete, stop
            if len(self.database) >= self.n_to_evaluate:
                self.done.set()

        # Store the result object for later processing
        self.simulation_results.append(result)


random_thinker = RandomThinker(
    queues, search_count, n_workers, search_space["smiles"].values
)
random_thinker.run()


from thinkers import BatchedThinker

output = widgets.Output()
display(output)
batched_thinker = BatchedThinker(
    queues=queues,
    n_to_evaluate=search_count,
    n_parallel=n_workers,
    initial_count=initial_count,
    batch_size=batch_size,
    molecule_list=search_space["smiles"].values,
    dashboard=output,
)
batched_thinker.run()

queues.send_kill_signal()
task_server.join()
print(f"Process exited with {task_server.exitcode} code")


with open(os.path.join(args.outdir, "random-results.json"), "w") as fp:
    for result in random_thinker.simulation_results:
        print(result.json(), file=fp)

with open(os.path.join(args.output, "batched-results.json"), "w") as fp:
    for result in batched_thinker.simulation_results:
        print(result.json(), file=fp)
    for result in batched_thinker.learning_results:
        # Write the learning results w/o the inputs and outputs
        #  because they are not JSON-serializable
        print(result.json(exclude={"inputs", "value"}), file=fp)

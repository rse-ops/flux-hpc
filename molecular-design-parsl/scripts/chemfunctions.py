"""Functions used to perform chemistry tasks in the Parsl workflow

While Parsl does offer the ability to run functions defined in a Jupyter notebook,
we define them here to keep the notebook cleaner   
"""
import os
from concurrent.futures import ProcessPoolExecutor
from functools import partial, update_wrapper
from typing import List

import numpy as np
import pandas as pd
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem
from qcelemental.models import OptimizationInput, Molecule, AtomicInput
from qcengine.compute import compute_procedure, compute
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline


# Make a global pool for this particular Python thread
#  Not a great practice, as it will not exit until Python does.
#  Useful on HPC as it limits the number of times we call `fork`
#   and we know the nodes where this run will get purged after tasks complete
n_workers = max(len(os.sched_getaffinity(0)) - 1, 1)  # Get as many threads as we are assigned to
_pool = ProcessPoolExecutor(max_workers=n_workers)

"""SIMULATION FUNCTIONS: Quantum chemistry parts of the workflow"""

_spec = {
    'model': {
        'method': 'GFN2-xTB',
        'basis': None
    },
    'keywords': {'accuracy': 0.05}
}


def generate_initial_xyz(mol_string: str) -> str:
    """Generate the XYZ coordinates for a molecule.
    
    Args:
        mol_string: SMILES string

    Returns:
        - InChI string for the molecule
        - XYZ coordinates for the molecule
    """

    # Generate 3D coordinates for the molecule
    mol = Chem.MolFromSmiles(mol_string)
    if mol is None:
        raise ValueError(f'Parse failure for {mol_string}')
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol, randomSeed=1)
    AllChem.MMFFOptimizeMolecule(mol)

    # Save geometry as 3D coordinates
    xyz = f"{mol.GetNumAtoms()}\n"
    xyz += mol_string + "\n"
    conf = mol.GetConformer()
    for i, a in enumerate(mol.GetAtoms()):
        s = a.GetSymbol()
        c = conf.GetAtomPosition(i)
        xyz += f"{s} {c[0]} {c[1]} {c[2]}\n"

    return xyz


def _run_in_process(func, *args):
    """Hack to make each execution run in a separate process. XTB or geoMETRIC is bad with file handles

    Args:
        func: Function to evaluate
        args: Input arguments
    """

    with ProcessPoolExecutor(max_workers=1) as exe:
        print(args)
        fut = exe.submit(func, *args)
        return fut.result()


def _compute_vertical(smiles: str) -> float:
    """Run the ionization potential computation

    Args:
        smiles: SMILES string to evaluate
    Returns:
        Ionization energy in Ha
    """

    # Make the initial geometry
    xyz = generate_initial_xyz(smiles)

    # Compute the neutral geometry
    #  Uses QCEngine (https://github.com/MolSSI/QCEngine) to handle interfaces to XTB
    mol = Molecule.from_data(xyz)
    opt_input = OptimizationInput(input_specification=_spec,
                                  initial_molecule=mol,
                                  keywords={"program": "xtb"})
    opt_res = compute_procedure(opt_input, "geometric", raise_error=True)

    # Compute the energy of the relaxed geometry in charged form
    charged_mol = Molecule.from_data(opt_res.final_molecule.to_string('xyz'), molecular_charge=1)
    input_spec = AtomicInput(molecule=charged_mol, driver='energy', **_spec)
    charged_res = compute(input_spec, 'xtb', raise_error=True)

    return charged_res.return_result - opt_res.energies[-1]


# Make versions that execute in separate processes
compute_vertical = partial(_run_in_process, _compute_vertical)
compute_vertical = update_wrapper(compute_vertical, _compute_vertical)
compute_vertical.__name__ = 'compute_vertical'

"""MACHINE LEARNING FUNCTIONS: Predicting the output of quantum chemistry"""


def compute_morgan_fingerprints(smiles: str, fingerprint_length: int, fingerprint_radius: int):
    """Get Morgan Fingerprint of a specific SMILES string.
    Adapted from: <https://github.com/google-research/google-research/blob/
    dfac4178ccf521e8d6eae45f7b0a33a6a5b691ee/mol_dqn/chemgraph/dqn/deep_q_networks.py#L750>
    Args:
      graph (str): The molecule as a SMILES string
      fingerprint_length (int): Bit-length of fingerprint
      fingerprint_radius (int): Radius used to compute fingerprint
    Returns:
      np.array. shape = [hparams, fingerprint_length]. The Morgan fingerprint.
    """
    # Parse the molecule
    molecule = Chem.MolFromSmiles(smiles)

    # Compute the fingerprint
    fingerprint = AllChem.GetMorganFingerprintAsBitVect(
        molecule, fingerprint_radius, fingerprint_length)
    arr = np.zeros((1,), dtype=np.bool)

    # ConvertToNumpyArray takes ~ 0.19 ms, while
    # np.asarray takes ~ 4.69 ms
    DataStructs.ConvertToNumpyArray(fingerprint, arr)
    return arr


class MorganFingerprintTransformer(BaseEstimator, TransformerMixin):
    """Class that converts SMILES strings to fingerprint vectors"""

    def __init__(self, length: int = 256, radius: int = 4):
        self.length = length
        self.radius = radius

    def fit(self, X, y=None):
        return self  # Do need to do anything

    def transform(self, X, y=None):
        """Compute the fingerprints
        
        Args:
            X: List of SMILES strings
        Returns:
            Array of fingerprints
        """

        my_func = partial(compute_morgan_fingerprints,
                          fingerprint_length=self.length,
                          fingerprint_radius=self.radius)
        fing = _pool.map(my_func, X, chunksize=2048)
        return np.vstack(fing)


def train_model(smiles: List[str], properties: List[float]):
    """Train a machine learning model using Morgan Fingerprints.
    
    Args:
        smiles: SMILES strings for each molecule
        properties: List of a property for each molecule
    Returns:
        A trained model
    """
    # Imports for python functions run remotely must be defined inside the function

    model = Pipeline([
        ('fingerprint', MorganFingerprintTransformer()),
        ('knn', KNeighborsRegressor(n_neighbors=4, weights='distance', metric='jaccard', n_jobs=-1))
        # n_jobs = -1 lets the model run all available processors
    ])

    return model.fit(smiles, properties)


def run_model(model, smiles):
    """Run a model on a list of smiles strings
    
    Args:
        model: Trained model that takes SMILES strings as inputs
        smiles: List of molecules to evaluate
    Returns:
        A dataframe with the molecules and their predicted outputs
    """
    pred_y = model.predict(smiles)
    return pd.DataFrame({'smiles': smiles, 'ie': pred_y})


if __name__ == "__main__":
    energy = compute_vertical('OC')

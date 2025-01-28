# -*- coding: utf-8 -*-
"""
This is implementation of model of corresponding to the pre-print `Large scale model of cat primary visual cortex`
Antolík, J., Cagnol, R., Rózsa, T., Monier, C., Frégnac, Y., & Davison, A. P. (2018).
https://www.biorxiv.org/content/10.1101/416156v5.abstract
"""
import matplotlib

matplotlib.use("Agg")

from mpi4py import MPI
from mozaik.storage.datastore import Hdf5DataStore, PickledDataStore
from parameters import ParameterSet
from analysis_and_visualization import perform_analysis_and_visualization_Katrin
from model import SelfSustainedPushPull
from experiments import create_experiments_KatrinFranke
import mozaik
from mozaik.controller import run_workflow, setup_logging, Global
import sys
from pyNN import nest


from mpi4py import MPI

mpi_comm = MPI.COMM_WORLD

import nest

nest.Install("stepcurrentmodule")

if len(sys.argv) > 2:

    data_store, model = run_workflow(
        "SelfSustainedPushPull", SelfSustainedPushPull, create_experiments_KatrinFranke
    )
    data_store.save()
else:
    print("Setting root direcotry to: " + str(Global.root_directory))
    Global.root_directory = sys.argv[1]
    data_store = PickledDataStore(load=True, parameters=ParameterSet(
        {'root_directory': sys.argv[1], 'store_stimuli': None}), replace=True)


if mpi_comm.rank == 0:
    print("Starting visualization")
    perform_analysis_and_visualization_Katrin(data_store)

# -*- coding: utf-8 -*-
import sys
from mozaik.meta_workflow.parameter_search import (
    CombinationParameterSearch,
    SlurmSequentialBackend,
)
import numpy
import time


experiment = "DanButts"

if experiment == "DanButts":

    # files = [
    #          'motion_cloud_batch_length=20000_seed=4367_res=220_spatial_sca=3.npy',
    #          'motion_cloud_batch_length=20000_seed=857_res=220_spatial_sca=3.npy',
    #          'motion_cloud_batch_length=20000_seed=4385_res=220_spatial_sca=3.npy',
    #          'motion_cloud_batch_length=20000_seed=1428_res=220_spatial_sca=3.npy',
    #          'motion_cloud_batch_length=20000_seed=6672_res=220_spatial_sca=3.npy',
    #          'motion_cloud_batch_length=20000_seed=6691_res=220_spatial_sca=3.npy',
    #          'motion_cloud_batch_length=20000_seed=5242_res=220_spatial_sca=3.npy',
    #          'motion_cloud_batch_length=20000_seed=7216_res=220_spatial_sca=3.npy',
    #          'motion_cloud_batch_length=20000_seed=4367_res=220_spatial_sca=6.npy',
    #          'motion_cloud_batch_length=20000_seed=857_res=220_spatial_sca=6.npy',
    #          'motion_cloud_batch_length=20000_seed=4385_res=220_spatial_sca=6.npy',
    #          'motion_cloud_batch_length=20000_seed=7216_res=220_spatial_sca=6.npy',
    #          'motion_cloud_batch_length=20000_seed=1428_res=220_spatial_sca=6.npy',
    #          'motion_cloud_batch_length=20000_seed=6672_res=220_spatial_sca=6.npy',
    #          'motion_cloud_batch_length=20000_seed=5242_res=220_spatial_sca=6.npy',
    #          'motion_cloud_batch_length=20000_seed=6691_res=220_spatial_sca=6.npy',
    #          'motion_cloud_batch_length=20000_seed=6691_res=220_spatial_sca=9.npy',
    #          'motion_cloud_batch_length=20000_seed=1428_res=220_spatial_sca=9.npy',
    #          'motion_cloud_batch_length=20000_seed=4367_res=220_spatial_sca=9.npy',
    #          'motion_cloud_batch_length=20000_seed=5242_res=220_spatial_sca=9.npy',
    #          'motion_cloud_batch_length=20000_seed=6672_res=220_spatial_sca=9.npy',
    #          'motion_cloud_batch_length=20000_seed=4385_res=220_spatial_sca=9.npy',
    #          'motion_cloud_batch_length=20000_seed=7216_res=220_spatial_sca=9.npy',
    #          'motion_cloud_batch_length=20000_seed=857_res=220_spatial_sca=9.npy'
    #          'motion_cloud_batch_length=10000_seed=857_res=220_spatial_sca=3.npy',
    #          'motion_cloud_batch_length=10000_seed=857_res=220_spatial_sca=6.npy',
    #          'motion_cloud_batch_length=10000_seed=5447_res=220_spatial_sca=9.npy',
    # ]

    # length = [20000,20000,20000,20000,20000,20000,20000,20000,20000,20000,20000,20000,20000,20000,20000,20000,20000,20000,20000,20000,20000,20000,20000,20000,10000,10000,10000]
    # trials = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,10,10,10]

    files = ["motion_cloud_batch_length=10000_seed=857_res=220_spatial_sca=3.npy"]
    length = [10000]
    trials = [10]

    i = 1

    for f, l, t in zip(files, length, trials):

        envexport = "--export=ALL,STIMFILE=%s,STIMLENGTH=%s,NUM_TRIALS=%s" % (f, l, t)

        CombinationParameterSearch(
            SlurmSequentialBackend(
                num_threads=1,
                num_mpi=16,
                slurm_options=[
                    "--hint=nomultithread",
                    "-x w[1-12,15,16]",
                    "-N 1-1",
                    envexport,
                ],
                path_to_mozaik_env="/home/antolikjan/virt_env/mozaiknew/bin/activate",
            ),
            {
                "trial": [i],
                "input_space.update_interval": [16],
                "sheets.retina_lgn.params.receptive_field.temporal_resolution": [16],
            },
        ).run_parameter_search()

        i = i + 1


elif experiment == "KatrinFranke":

    CombinationParameterSearch(
        SlurmSequentialBackend(
            num_threads=1,
            num_mpi=16,
            slurm_options=["--hint=nomultithread", "-x w[1-12,15,16]", "-N 1-1"],
            path_to_mozaik_env="/home/antolikjan/virt_env/mozaiknew/bin/activate",
        ),
        {
            "trial": [1],
            "input_space.update_interval": [10],
            "sheets.retina_lgn.params.receptive_field.temporal_resolution": [10],
            "null_stimulus_period": [300],
            "experiments_global_frame_offset" : [0,1,2,3,4,5,6,7,8,9,10,11],
            "num_presentation_trials" : [303]
        },
    ).run_parameter_search()

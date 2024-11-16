#!/usr/local/bin/ipython -i
from mozaik.experiments import *
from mozaik.experiments.vision import *
from parameters import ParameterSet
import os


def create_experiments_DanButts(model):

    return [
        MeasurePixelMovieFromFile(
            model,
            ParameterSet(
                {
                    "movie_path": "/home/antolikjan//projects/mozaiknew/DATASETS/LSV1M_for_ML_MotionClouds/",
                    "movie_name": str(os.environ["STIMFILE"]),
                    "num_trials": int(os.environ["NUM_TRIALS"]),
                    "shuffle_stimuli": False,
                    "width": 11,
                    "movie_frame_duration": 16,
                    "global_frame_offset": 0,
                    "images_per_trial": int(os.environ["STIMLENGTH"]),
                    "num_presentation_trials": 1,
                }
            ),
        ),
    ]


def create_experiments_KatrinFranke(model,experiment_parameters):
    global_frame_offset = experiment_parameters['global_frame_offset']
    num_presentation_trials = experiment_parameters['num_presentation_trials']

    return [
        MeasurePixelMovieFromFile(
            model,
            ParameterSet(
                {
                    "movie_path": "/home/antolikjan//projects/mozaiknew/DATASETS/LSV1M_model_for_Katrin/",
                    "movie_name": "imgs_grayscale.npy",
                    "num_trials": 1,
                    "shuffle_stimuli": False,
                    "width": 11,
                    "movie_frame_duration": 120,
                    "global_frame_offset": global_frame_offset,
                    "images_per_trial": 15,
                    "num_presentation_trials": num_presentation_trials,
                }
            ),
        ),
    ]

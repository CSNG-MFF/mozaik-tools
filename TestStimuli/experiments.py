#!/usr/local/bin/ipython -i 
from mozaik.experiments import *
from mozaik.experiments.vision import *
from mozaik.sheets.population_selector import RCRandomPercentage
from parameters import ParameterSet
    
def create_experiments(model):
    return              [
                            #Spontaneous Activity 
                            #NoStimulation(model,duration=2*147*7),
                            #MeasureSpontaneousActivity(model,2*147*7,1),
                            #MeasureOrientationTuningFullfield(model,num_orientations=1,spatial_frequency=0.8,temporal_frequency=2,grating_duration=4*147*7,contrasts=[0,2,4,8,16,32,64,100],num_trials=10),

                            MeasurePixelMovieFromFile(model,ParameterSet({
                                 'duration' : 70,
                                 'movie_path' : './',
                                 'movie_name' : 'example_pixel_movie.npy',
                                 'num_trials' : 1,
                                 'shuffle_stimuli' : False
                             })),

            
                        ]


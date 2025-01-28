#!/usr/local/bin/ipython -i
from mozaik.experiments import *
from mozaik.experiments.vision import *
from mozaik.sheets.population_selector import RCRandomPercentage
from parameters import ParameterSet
from mozaik.experiments.electrical_stimulation import RandomSingleNeuronStepCurrentInjection, RandomSingleNeuronStepCurrentInjectionDuringDriftingSinusoidalGratingStimulation

def create_experiments(model,p):
    return [
        # NoStimulation(model,duration=2*147*7),
        MeasureSpontaneousActivity(model,ParameterSet({'duration':2*147*7,'num_trials':1,'shuffle_stimuli' : False})),
        MeasureOrientationTuningFullfield(model,ParameterSet({'num_orientations' : 1,'spatial_frequency': 0.8,'temporal_frequency' : 2,'grating_duration': 2*147*7,'contrasts' : [0,2,4,8],'num_trials' :1,'shuffle_stimuli' : False})),

        #RandomSingleNeuronStepCurrentInjection(
        #    model,
        #    ParameterSet(
        #        {
        #                'duration': 500,
        #                'current' : 0.06,
        #                'sheet' : "V1_Exc_L4",
        #                'num_neurons' : 2,
        #                'num_trials' : 1, 
        #                'experiment_random_seed' : 513,
        #                'stimulation_configuration' : ParameterSet({
        #                        'component' :  'mozaik.sheets.population_selector.RCAllWihinBoundry',
        #                        'params' : ParameterSet({
        #                            'size': 2000,
        #                            'offset_x' : 0, 
        #                            'offset_y' : 0, 
        #                    }),
        #                }),
        #        }
        #    ),
        #),


    ]

import multiprocessing as mp
from bluepyopt.deapext.optimisationsCMA import DEAPOptimisationCMA
from evaluator import define_evaluator
import json
import os

######################################
# Configuration for the optimization #
######################################

offspring_size = 12                 # Size of the population used by the optimizer
timeout = 72000                     # Hard cut-off for the evaluation of an individual (in seconds)
optimiser_seed = 7                  # random seed for the optimiser
optimiser_sigma = 0.3               # width of the search at the first generation of the optimisation, default: 0.4
max_ngen = 200                      # Maximum number of generation of the optimiser
                                    
continue_cp = False                 # Should the optimisation resume from the informed checkpoint file 
                                    # False -> optimization starts from scratch
                                    # True -> optimization continues from the checkpoint file
cp_filename = './20250328-192103_Optimization/opt_check.pkl'
                                    # Path to the checkpoint file of the optimisation, used only if continue_cp is True 

model_dir = '[DIR_TO_MODEL]'        # Path to the model directory, from there the mopzaik simulations are run
                                    # e.g. '/home/user/mozaik-models/LSV1M'
                                    # If the optimization is run from the model directory, this can be set to './'
os.chdir(model_dir)

########################
# End of configuration #
########################

run_script = 'run_optimization_experiment.py'
parameters_url = 'param_optim/defaults'
config_optimisation = './param_optim/config_optimisation'


with open(config_optimisation) as f:
    opt_config = json.load(f)

# Load optimiser centroid - the initial point of the optimisation
optimiser_centroid = []
for key in opt_config["parameters"].keys():
    if key in opt_config["optimiser_centroid"]:
        optimiser_centroid.append(opt_config["optimiser_centroid"][key])
    else:
        raise KeyError(f"Key {key} not found in optimiser_centroid in config_optimisation file {config_optimisation}")
        # TODO: it would be nice to use default parameter value of the model instead of raising an error


evaluator = define_evaluator(
    run_script=run_script,
    parameters_url=parameters_url,
    timeout = timeout,
    config_optimisation=config_optimisation,
)

if not continue_cp:
    cp_filename = f"./{evaluator.optimization_id}/opt_check.pkl"       # Path to the checkpoint file of the optimisation
else:
    raise Exception("Please inform the path to the last checkpoint file here !")

map_function = mp.Pool(processes=offspring_size).map

optimizer = DEAPOptimisationCMA(
    evaluator=evaluator,
    use_scoop=False,
    seed=optimiser_seed,
    offspring_size=offspring_size,
    map_function=map_function,
    selector_name="single_objective",
    use_stagnation_criterion=False,
    sigma=optimiser_sigma,
    centroids=[optimiser_centroid]
)

optimizer.run(
    max_ngen=max_ngen,
    cp_filename=cp_filename,
    cp_frequency=1,
    continue_cp=continue_cp,
)

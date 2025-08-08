This tool is made for automatic optimization of mozaik models parameters.
The original development and copyrights go to Tanguy Damart (original repository: [DrTaDa/OptLSV1M](https://github.com/DrTaDa/OptLSV1M/tree/main)).
This directory is minimal and cleaned up version of the original with few small updates and new targets.

It is expected that one already has a mozaik model for optimization prepared elsewhere. 
In this folder no model is provided, just scripts for controlling optimization.

**Big picture story:**
One defines set a parameters that can be altered and set of *targets* that the model should reach. After running a simulation, for each target a *value* is calculated, Comparing it with the *target value* a *score* is computed, roughly according to following formula

score = (target value - value) / norm.

Optimizer then estimates how to alter parameters in the next step/generation such that the overall scores are minimized.


In general one main evaluating script will be run. This script will run a set of simulations with randomly generated parameters. 
Once the simulations finish, it evaluates the results, removes the simulation directory and saves the used parameters and resulting
scores on specified targets. Once evaluation is done a new generation of simulation is generated.

# Running optimization
Before running optimization it is important to first prepared the model (parameters), setup the optimization method and parameters and targets for which to optimize.

### Mozaik model configuration

1. In the model picked for optimization copy, create `param_optim` folder. One can *either* use script `prepare_model_for_optimization.py` *or* do it manually
    - if using the *script*:
        1. Set up the configuration of the desired model inside the script
        1. Run `python prepare_model_for_optimization.py` from the optimization folder
    - if doing it *manually*:
        1. Copy the default parameters into `param_optim` folder 
        1. Change the urls (sheet urls, recorders), 
        1. Update the recorders such that they replicate `param_optim/recorders`
        1. Copy `param_optim/config_optimisation` from Optimization folder
1. Copy following files into model directory (if you did not use the script in previous step, which already copied the files)
    - `run_optimization_experiment.py`
    - (**Optionally** one can copy the whole content of `Optimization` folder into model folder - see below)
1. Update virt_env in following files:
    - `optimisation.sbatch`
    - `evaluator.py` in function `define_evaluator`
1. Mozaik tweaks
    - When too many parameters are optimized, the default name of directories are too long, which results in crashes. The default directory name has to be limited.

---
For configuration one can go with one of the two approaches:
- optimization files **Inside of model directory**
    - That means move all the optimization files into model folder.
    - Probably better when having separate venv for each model (do not have to update virtenv in `evaluator.py` all the time).
- optimization files **Outside of model directory**
    - Keeping one optimization folder common to multiple model. Easier for managing and updating optimization process.

### Optimization configuration
1. In `param_optim/config_optimization` define:
    - Parameters which can be modified are under `parameters` and a range of values should be provided
    - Initial point for optimization is under `optimiser_centroid`.
    - [Targets](#targets) that should be optimized are under `targets`. Each target is a dictionary with following items:
        - `class`: TargetClass
        - `target_value`: float or range (depending on TargetClass)
        - `sheet_name`: string for filtering data_store
        - `norm`: float (deviation from `target_value` by 1 norm = 1 score point)
        - `max_score`: int (default 20)
1. In `run_optimization.py` setup optimization method
    - `offspring_size` - number of simulations per generation
    - `timeout` - timeout for a generation (after the timeout, jobs are cancelled and maximal scores are returned)
        - WARNING: it times also the time in the time in queue! (so be generous)
    - `optimiser_seed` - seed for optimizer
    - `optimiser_sigma` - controls the spread of parameters from initial point
        - WARNING: if sigma is high (> 0.5) or parameter range is big, the chosen parameters may lead to explosions (if the optimization is dominated by explosions consider lowering this parameter)
    - `max_ngen` - maximum number of generations to use
    - `continue_cp` - bool, False = start optimization from scratch, True = continue from previous optimization
    - `cp_filename` - str, directory with optimization checkpoint file to continue from, if `continue_cp` is False it is not used
    - `model_dir` - directory to the model (when optimization is in different folder, path to the model is needed, such that the optimization can be run from the model directory)

### Running optimization
Run optimization as simply as

`sbatch optimisation.sbatch`

# Targets
Each target for optimization needs to have specified:
- `class` : name of the Target class
- `target value` : float or range depending on Target class
- `sheet_name` : sheet for which to compute the target
- `norm` : relative 
- `max_score` : maximal score for the target. (If simulation fails and optimizer is unable to compute score it will also return max_score)

### List of currently defined targets
`SpontActivityTarget`
- This target calculates spontaneous activity from spikes of all neurons in the sheet
- target_value : range of values (any value within the rage gives score 0)
`IrregularityTarget`
- This target calculates mean irregularity (coefficient of variation) from all the neurons in the sheet 
- target_value : float, (1 = irregular), (Bounded target - anything above this number gives score 0)
`SynchronyTarget`
- This target calculates synchrony as mean correlation coefficient between neuron PSTHs. Neurons used for the statistics must meet following conditions:
    - placed within a centered square 3x3
    -  have at least 6 spikes during NoStimulus experiment 
- target_value : 0
`OrientationTuningPreferenceTarget`
- This target calculates orientation preference as a ratio of mean activity for drifting grating of optimal orientation and mean activity for drifting grating of orthogonal orientation.
- target_value :  5 (Bounded target - anything above this number gives score 0)
`OrientationTuningOrthoHighTarget`
- This target calculates the difference  of spontaneous activity and activity for drifting grating of orientation orthogonal to optimal orientation for high contrast
- target_value : 0
`OrientationTuningOrthoLowTarget`
- This target calculates the difference  of spontaneous activity and activity for drifting grating of orientation orthogonal to optimal orientation for low contrast
- target_value : 0
`SizeTuning`
- This target calculates size tuning as a fraction of cells that  show suppression. Suppression is defined here as a ratio between firing rate in response to disk of radius 1.25 and full field grating. If the ratio is greater than 1.1, the cell is assumed to show suppression.
- target_value : 0.7 (Bounded target - anything above this number gives score 0)
`ConductanceRatio`
- This target calculates the ratio of Inhibitory to Excitatory synaptic conductances.
- target_value : 5.0
`ModulationRatio`
- This target calculates the Modulation Ratio (F1/F0) from spiking activity
- target_value : 1.5 (simple cells), 0.5 (complex cells)

# Tricks & Tips
- usually one simulation goes around ~ 1h, more than 2h is suspicious something went wrong
- when a simulation explodes the rest of experiments is not presented and instead maximum scores are given for the targets
- when simulation explodes it usually takes long time (that is why a short NoStimulus is presented first to check for explosions)
- Use lower density for initial search
- Clean up slurm log files! After few generations the optimization folder can get very large due to the log files.
- After running the optimization, run the other protocols for the model (spont, orientation tuning, size tuning). 
The choice of recorders and single trial for each experiment does not replicate the results for these protocols

# Content of the directory

`prepare_model_for_optimization.py`
- script that will copy the files into a model directory (it would make the param_optim file structure)

`optimisation.sbatch`
- sbatch file for running the optimization
- It is better to run the main optimization script on one of the bigger nodes (it can be loading multiple datastores in parallel which sometimes crashes due to memory on small nodes)

`run_optimization.py`
- script that controls the optimization.

`evaluator.py`
- Defines evaluator class, which is responsible for evaluating mozaik simulations, calculating scores.

`targets.py`
- collection of targets for which to optimize.

`utils.py`
- collection of various useful functions for running the optimization as well for following inspection

`run_optimization_experiment.py`
- File with experiments defined for the optimization
- It contains the minimal experiments such that it can quickly produce results for optimization

`param_optim/config_optimization`
- Here you specify the optimization Targets and parameters to play with 
- Example config file for optimization.
- This file is copied when using `prepare_model_for_optimization.py` into the model directory

`param_optim/recorder`
- Recorder used for optimization
- At the moment recorders are recording all spikes of all neurons and synaptic conductance for selected grid in the center (same as in param_spont)

`optimization_analyze.ipynb`
- jupyter notebook for checking the results of optimization

`optimization_evaluate_data_store.ipynb`
- jupyter notebook for debugging
- sometimes the optimization crashes, this notebook evaluates the data_store to assess whether it was problem of mozaik simulation or optimization set up

`optimization_inspect_spont_OT_ST.ipynb`
- jupyter notebook for further analyzing orientation tunning etc.
- (will be added)


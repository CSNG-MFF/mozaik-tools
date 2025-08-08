"""
This script creates `param_optim` directory for a specified model.
It sets up the necessary configuration files and directories for running optimizations.

What it does:
- Creates `param_optim` directory in the specified model directory.
    - `param_optim` is a copy of a given base param directory (default = `param`).
    - recorders are changed to match `Optimization/param_optim/recorders`
    - `Optimization/param_optim/config_optimisation` is moved to the model `param_optim` directory.
- Copies `run_optimization_experiment.py` to the model directory.

"""

from pathlib import Path
import shutil

#################
# Configuration #
#################

model_dir = Path('path/to/model')       # eg. Path('/home/user/mozaik-models/LSV1M')
base_param = 'param'                    # Name of param folder to copy from
optim_param = 'param_optim'             # Name of param folder to create (the name `param_optim` is expected by the optimization scripts)

exist_ok = False                        # Set to True if you want to overwrite existing `param_optim` directory

# TODO: option to copy the whole `Optimization` directory to the model directory

########################
# End of configuration #
########################

# source_dir is Optimization directory where this script is located
source_dir = Path(__file__).resolve().parent

# Create the `param_optim` directory in the model directory
(model_dir / optim_param).mkdir(exist_ok=exist_ok)

# Copy the base parameter directory to the optimization parameter directory
# Also identify recorder files
recorder_list = []
for file in (model_dir / base_param).glob('*'):
    if file.is_dir():
        raise IsADirectoryError(f"Expected a file, but found a directory: {file}")

    src_file = model_dir / base_param / file.name
    dest_file = model_dir / optim_param / file.name
    with open(src_file, 'r') as src, open(dest_file, 'w') as dest:
        for line in src:
            if 'url(' in line:
                line = line.replace(base_param, optim_param)
                if 'recorders' in line:
                    # feel free to make this more robust/use regex
                    recorder_name = line.replace(" ","").replace("\n","").replace("'","").replace('"',"").split("/")[-1].rstrip("),")
                    if not (model_dir / base_param / recorder_name).exists():
                        # Probably due to bad parsing
                        raise FileNotFoundError(f"Recorder file {recorder_name} not found in {base_param} directory.")
                    recorder_list.append(recorder_name)
            dest.write(line)
    print(f"Copied {src_file} to {dest_file}")

# Update the recorders in the copied files
src_recorder = source_dir / 'param_optim' / 'recorder'
for recorder_name in recorder_list:
    dest_recorder = model_dir / optim_param / recorder_name
    if dest_recorder.exists():
        shutil.copy(src_recorder, dest_recorder)
        print(f"Updated recorder {recorder_name} in {dest_recorder}")
    else:
        print(f"Recorder {recorder_name} not found in {src_recorder}")

# Move the configuration file to the model's `param_optim` directory
shutil.copyfile(
    source_dir / 'param_optim' / 'config_optimisation',
    model_dir / optim_param / 'config_optimisation'
)

# Move `run_optimization_experiment.py` to the model directory
shutil.copyfile(
    source_dir / 'run_optimization_experiment.py',
    model_dir / 'run_optimization_experiment.py'
)

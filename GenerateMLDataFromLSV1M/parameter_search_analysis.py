import sys
from mozaik.meta_workflow.parameter_search import parameter_search_run_script_distributed_slurm
assert len(sys.argv) == 2
directory = sys.argv[1]

parameter_search_run_script_distributed_slurm("SelfSustainedPushPull", directory, 'run_KatrinFranke.py', 32,'/home/antolikjan/virt_env/mozaikluca/bin/activate',nodes_to_exclude="w[1-8,10,12]")
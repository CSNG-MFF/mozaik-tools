import os
import mozaik
from mozaik.analysis.technical import NeuronAnnotationsToPerNeuronValues, ExportRawSpikeData
from mozaik.storage.queries import *

logger = mozaik.getMozaikLogger()

def perform_analysis_and_visualization(data_store):
    dsv = param_filter_query(data_store,st_name="PixelMovieFromFile")
    ExportRawSpikeData(dsv,ParameterSet({'file_name' : "responses_" + str(os.environ['STIMFILE'])})).analyse()


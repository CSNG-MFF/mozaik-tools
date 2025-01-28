import sys

sys.path.append("/home/jan/projects/mozaik/")
import numpy
from parameters import ParameterSet
from mozaik.models import Model
from mozaik import load_component
from mozaik.space import VisualRegion
from mozaik.connectors.meta_connectors import GaborConnector

class TestStimuliModel(Model):

    required_parameters = ParameterSet(
        {
            "sheets": ParameterSet(
                {
                    "retina_lgn": ParameterSet,
                }
            ),
            "visual_field": ParameterSet,
        }
    )

    def __init__(self, simulator, num_threads, parameters):
        Model.__init__(self, simulator, num_threads, parameters)

        RetinaLGN = load_component(self.parameters.sheets.retina_lgn.component)
        CortexExcL4 = load_component(self.parameters.sheets.l4_cortex_exc.component)
        
        # Build and instrument the network
        self.visual_field = VisualRegion(
            location_x=self.parameters.visual_field.centre[0],
            location_y=self.parameters.visual_field.centre[1],
            size_x=self.parameters.visual_field.size[0],
            size_y=self.parameters.visual_field.size[1],
        )
        self.input_layer = RetinaLGN(self, self.parameters.sheets.retina_lgn.params)

        # which neurons to record
        tr = {
            "spikes": "all",
            "v": numpy.arange(0, 60, 1),
            "gsyn_exc": numpy.arange(0, 60, 1),
            "gsyn_inh": numpy.arange(0, 60, 1),
        }

        self.input_layer.sheets["X_ON"].to_record = tr  #'all'
        self.input_layer.sheets["X_OFF"].to_record = tr  #'all'

        cortex_exc_l4 = CortexExcL4(self, self.parameters.sheets.l4_cortex_exc.params)

        # initialize afferent layer 4 projections
        GaborConnector(
            self,
            self.input_layer.sheets["X_ON"],
            self.input_layer.sheets["X_OFF"],
            cortex_exc_l4,
            self.parameters.sheets.l4_cortex_exc.AfferentConnection,
            "V1AffConnection",
        )

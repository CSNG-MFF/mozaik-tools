A simple very economic mozaik simulaton setup, where you insert your stimulation experiment (into expriments.py) and will receive a video of the stimulus actually presented on the retina.

It is pretty much just the LGN/retina model with very small resolution coupled with RetinalMovie analysis and visualisation.

## Instructions

1. Insert your new stimulation experiment into experiments.py.
2. Execute:
    python run.py nest 2 param/defaults 'test'
3. New directory will be created which will contain 'mov.html' containing the movie. You can open it with any web browser.
4. Individual frames of the stimulus will be in 'mov_frames' subdirectory

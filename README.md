# BaggageAI Computer Vision Hiring Assignment

The program crops a foreground image and paste it over Background image.

there are some augmentations applied on the forground image those are listed below.

- scaling
- rotation
- tranparency

The program is robust enough to perform all these augmentations and pastes the threat objects at random locations. thus
creating new data at every runtime.

## requirements

to install requirements run following command

```buildoutcfg
pip install -r requirements.txt
```

## Usage

The program is divided in two stages cropping stage and the merging stage.

### cropping stage

In this stage cropping of the threat image takes place. To do this the all required threat images has to be on same
folder.

default threat path is "threat_images" and default output path is 'cropped'.

to run the cropping script run following command

```buildoutcfg
python crop_threat.py
```

After running the program to crop the threat a rectangle has to drawn. this can be done by dragging the mouse pointer
from top-left of the threat object to bottom-right of the object. once the region of interest is drawn to save the
cropped region 's' can be pressed, to clear region of interest 'r' can be pressed and for next image 'q' can be pressed.

### pasting/merging stage

in this stage every threat object is pasted on every single background object.

default paths are as follows:

- for cropped threats, 'cropped'
- for background images, 'background_images'
- for outputs, 'output'

to run merging script run following command

```buildoutcfg
python run.py
```

after running this script the merged images can be found in the 'output' folder

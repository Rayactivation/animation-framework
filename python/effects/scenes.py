import example
import bitmap
from animation_framework.framework import Scene

SCENES = [
    #Scene(
    #    "movingslice",
    #    effects=[MovingSlice()]
    #),
    Scene(
        "Letters",
        effects=[
            example.SolidBackground(color=(150,0,0)),
            bitmap.MidiLetterListener()
        ]
    ),

]
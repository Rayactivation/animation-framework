import example
import bitmap
from animation_framework.framework import Scene, MultiEffect, Effect
from animation_framework.state import STATE

class MidiListener(MultiEffect):
    def __init__(self, clazz, zargs):
        MultiEffect.__init__(self)
        self.clazz = clazz
        self.zargs = zargs

    def before_rendering(self, pixels, t):
        super(MidiListener, self).before_rendering(pixels, t)
        for data in STATE.osc_data.current['midi']:
            self.add_effect(self.clazz(data))

SCENES = [
    #Scene(
    #    "movingslice",
    #    effects=[MovingSlice()]
    #),
    #Scene(
    #    "Letters",
    #    effects=[
    #        example.SolidBackground(color=(150,0,0)),
    #        bitmap.MidiLetterListener()
    #    ]
    #),
    Scene(
        "DrumHarderRows",
        effects=[
            example.SolidBackground(color=(60,0,0)),
            bitmap.StaticBitmap(bitmap.CACHED_WORDS['DRUM HARDER'], (100,100,100), -1, 1),
            #example.MovingColor()
            MidiListener(example.DrumHitRow, [])
        ]
    )

]
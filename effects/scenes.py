from effects import bitmap, example, midi_effects

from animation_framework.model import Scene, MultiEffect
from animation_framework.state import STATE
from animation_framework.midi.midi_utils import MidiLauncher

DURATION=30

class MidiListener(MultiEffect):
    def __init__(self, clazz):
        MultiEffect.__init__(self)
        self.clazz = clazz

    def before_rendering(self, pixels, t):
        super(MidiListener, self).before_rendering(pixels, t)
        for data in STATE.osc_data.current['midi']:
            self.add_effect(self.clazz(data))

class SuperBass(MultiEffect):
    def before_rendering(self, pixels, t):
        super(SuperBass, self).before_rendering(pixels, t)
        for data in STATE.osc_data.current['midi']:
            if(data.note==36): #'B'ass
                self.add_effect(bitmap.DrawMovingBitmap(bitmap.BIG_LETTERS['B'], (255, 255, 255), -1, 0))

class FlashTony(MultiEffect):
    def before_rendering(self, pixels, t):
        super(FlashTony, self).before_rendering(pixels, t)
        for data in STATE.osc_data.current['midi']:
            if(data.note==36): #'B'ass
                self.add_effect(bitmap.FlashBitmap(bitmap.CACHED_WORDS['TONYx3'], (255, 255, 255), -1, DURATION, 0))

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
            example.SolidBackground(color=(60, 0, 0)),
            bitmap.StaticBitmap(bitmap.CACHED_WORDS['DRUM HARDER'], (100, 100, 100), -1, 1),
            #example.MovingColor()
            MidiLauncher(midi_effects.DrumHitRow)
        ]
    ),
    Scene(
        "SuperTony",
        effects=[
            example.SolidBackground(color=(255, 0, 0)),
            FlashTony(),
            MidiLauncher(midi_effects.DrumHitRow)
        ]
    )
]
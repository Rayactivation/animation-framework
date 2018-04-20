import random
from animation_framework.framework import Effect, Scene, MultiEffect
from animation_framework.state import STATE

LETTERS = {
    # 8x4
    'B': [ [0,0],[1,0],[2,0],  [0,1],[3,1],  [0,2],[3,2],  [0,3],[1,3],[2,3],  [0,4],[1,4],[2,4],  [0,5],[3,5],  [0,6],[3,6],  [0,7],[1,7],[2,7] ],
    #3x1
    'T': [ [0,0],[1,0],[2,0],  [1,1],  [1,2] ] 
}

class DrawBitmap(Effect):
    def __init__(self, bitmap, color, direction=-1):
        Effect.__init__(self)
        self.color = color
        #TODO: buffer zone
        self.bitmap = bitmap
        self.direction = direction
        self.col = 0 if direction > 0 else STATE.layout.rows-1

    def next_frame(self, pixels, t):
        #TODO faster.
        for point in self.bitmap:
            pixels[self.col-point[0],point[1]]=self.color
        self.col += self.direction


    def is_completed(self, t):
        # TODO - edge cases, padding
        return self.col < 0 or self.col >= STATE.layout.rows

class MidiLetterListener(MultiEffect):
    def before_rendering(self, pixels, t):
        super(MidiLetterListener, self).before_rendering(pixels, t)
        for data in STATE.osc_data.current['midi']:
            #self.add_effect(MovingColor(data,slice(0,None)))
            #self.add_effect(DrumHitRow(data))
            if(data.note==36): #'B'ass
                self.add_effect(DrawBitmap(LETTERS['B'], (255,255,255)))
            else:
            #elif(data.note in [43,47,48]): #'T'om
                self.add_effect(DrawBitmap(LETTERS['T'], (255,255,255)))
            #else:
            #    self.add_effect(DrumHitRow(data))

import random
import numpy as np
from animation_framework.framework import Effect, Scene, MultiEffect
from animation_framework.state import STATE

BIG_LETTERS = {
    # 8x4
    'B': [ [0,0],[1,0],[2,0],  [0,1],[3,1],  [0,2],[3,2],  [0,3],[1,3],[2,3],  [0,4],[1,4],[2,4],  [0,5],[3,5],  [0,6],[3,6],  [0,7],[1,7],[2,7] ],
}

SMALL_LETTERS = {
    #3x3
    'H': [ [0,0],[2,0],  [0,1],[1,1],[2,1],  [0,2],[2,2] ],
    'O' : [ [0,0],[1,0],[2,0],  [0,1], [2,1],  [0,2], [1,2], [2,2] ],
    'T': [ [0,0],[1,0],[2,0],  [1,1],  [1,2] ]
}

#5x5
LETTERS = {
    'C': [ [1,0],[2,0],[3,0],[4,0],  [0,1],  [0,2],  [0,3],  [1,4],[2,4],[3,4],[4,4] ],  #Really long. Maybe add another left vertical column
    'M': [ [0,0],[4,0],  [0,1],[1,1],[3,1],[4,1],  [0,2],[2,2],[4,2],  [0,3],[4,3],  [0,4],[4,4] ],
    'N': [ [0,0],[4,0],  [0,1],[1,1],[4,1],  [0,2],[2,2],[4,2],  [0,3],[3,3],[4,3],  [0,4],[4,4] ],
    'O': [ [1,0],[2,0],[3,0],  [0,1],[4,1],  [0,2],[4,2],  [0,3],[4,3],  [1,4],[2,4],[3,4] ],
    'T': [ [0,0],[1,0],[2,0],[3,0],[4,0],  [2,1],  [2,2], [2,3], [2,4] ],
    'Y': [ [0,0],[4,0],  [1,1],[3,1],  [2,2],  [2,3],  [2,4] ]
}

#6X6
LETTERS_SIX = {
    'M': [[c,r] for r in range(6) for c in [0,5]] + [[1,1],[2,2],[3,2],[4,1]],
    'N': [[c,r] for r in range(6) for c in [0,5]] + [[c,c] for c in range(1,5)],
    'O': [[c,r] for r in [0,5] for c in range(1,5)] + [[c,r] for r in range(1,5) for c in [0,1,4,5]] + [[c,r] for r in [1,4] for c in range(2,4)],
    'T': [[c,r] for r in [0,1] for c in range(6)] + [[c,r] for r in range(2,6) for c in [2,3]],
    'Y': [[c,c] for c in [0,1]] + [[c,5-c] for c in [4,5]] + [[c,r] for c in [2,3] for r in range(2,6)]
}

def createWord(bitmaps, space_per_letter):
    #TODO: use reduce
    word = []
    offset=0
    for bitmap in bitmaps:
        word += map(lambda point: [point[0]+offset, point[1]], bitmap)
        offset += space_per_letter
    return word

CACHED_WORDS = {
    'TONY': createWord([LETTERS_SIX[L] for L in "TONY"], 7)
}

class FlashBitmap(Effect):
    def __init__(self, bitmap, color, direction, top_row, left_col, duration):
        Effect.__init__(self)
        self.color = color
        self.timer = duration
        self.bitmap = []
        left_offset = left_col if direction>0 else STATE.layout.rows-left_col
        self.bitmap = map(lambda point: [point[0]*direction+left_offset, point[1]+top_row], bitmap)

    def next_frame(self, pixels, t):
        for point in self.bitmap:
            pixels[point[0],point[1]] = self.color
        self.timer = self.timer-1

    def is_completed(self, t):
        return self.timer < 0

class DrawMovingBitmap(Effect):
    def __init__(self, bitmap, color, direction=-1, top_row=0):
        Effect.__init__(self)
        self.color = color
        #TODO: buffer zone
        self.bitmap = map(lambda point: [point[0]*direction,point[1]+top_row], bitmap)
        self.direction = direction
        self.col = 0 if direction > 0 else STATE.layout.rows-1

    def next_frame(self, pixels, t):
        #TODO faster (numpy manipulations?)
        for point in self.bitmap:
            pixels[self.col+point[0],point[1]]=self.color
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
                #self.add_effect(DrawMovingBitmap(LETTERS_SIX['M'], (255,255,255), -1, 1))
                self.add_effect(FlashBitmap(CACHED_WORDS['TONY'], (255,255,255), -1, 1, 10, 30))
            #else:
            #    self.add_effect(DrumHitRow(data))

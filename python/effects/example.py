import random
from animation_framework.framework import Effect, Scene, MultiEffect
from animation_framework.state import STATE

class SolidBackground(Effect):
    """Always return a singular color. Can be bound top/bottom and
    left-right (wrap-around not supported yet)
    """

    def __init__(self, color=(255, 0, 0), start_col=0, end_col=None, start_row=0, end_row=None):
        Effect.__init__(self)
        self.color = color
        self.slice = (slice(start_row, end_row), slice(start_col, end_col))
        print "Created with color", self.color

    def next_frame(self, pixels, t):
        pixels[self.slice] = self.color

class MovingSlice(Effect):
    """Always return a singular color. Can be bound top/bottom and
    left-right (wrap-around not supported yet)
    """

    def __init__(self, color=(255, 0, 0), start_row=0, length=10, col=0):
        Effect.__init__(self)
        self.color = color
        self.current_row = start_row
        self.col = col
        self.length= length

    def next_frame(self, pixels, t):
        if self.current_row+self.length>113:
            pixels[self.current_row:] = self.color
            pixels[0:self.length+self.current_row-113] = self.color
        else:
            pixels[self.current_row:self.current_row+self.length] = self.color
        self.current_row = (self.current_row) + 1 % 113


class SelfDestructingSolidColor(Effect):
    def __init__(self, note, velocity):
        Effect.__init__(self)
        #self.color = tuple(self._get_color(note, min(velocity*2,200), i) for i in range(3))
        self.color = (0,0,min(velocity*2,200))
        self.rendered = 3

    def next_frame(self, pixels, t):
        pixels[:] = self.color
        self.rendered -= 1

    def is_completed(self, t):
        return self.rendered <= 0

    def _get_color(self, note, velocity, param):
        return velocity if note%3 == param else 0


class MovingColor(Effect):
    def __init__(self, drum_hit, columns):
        Effect.__init__(self)
        #self.color = tuple(self._get_color(note, min(velocity*2,255, 80), i) for i in range(3))
        self.color = (
            0,
            self._get_color(drum_hit.note, min(drum_hit.velocity*2,255, 80), 1),
            self._get_color(drum_hit.note, min(drum_hit.velocity*2,255, 80), 0),
            )
        self.location = 0
        self.columns = columns

    def next_frame(self, pixels, t):
        #pixels[self.location:self.location+2,:] = self.color
        pixels[STATE.layout.rows/2+self.location:STATE.layout.rows/2+self.location+2,self.columns] = self.color
        pixels[STATE.layout.rows/2-self.location-2:STATE.layout.rows/2-self.location,self.columns] = self.color
        self.location += 1

    def is_completed(self, t):
        return self.location >= STATE.layout.rows/2-1

    def _get_color(self, note, velocity, param):
        return velocity if note%2 == param else 0

class DrumHitRow(Effect):
    def __init__(self, note):
        Effect.__init__(self)
        self.color = (255,255,255)
        self.column_location=STATE.layout.rows-1
        self.row=0
        drum_hit = note.note
        if(drum_hit==36):
            #bass
            self.row=7
        elif(drum_hit in [42, 44, 46, 85, 86]):
            #high hat
            self.row=0
            if(drum_hit==42):
                self.color = (0,255,0)
            elif(drum_hit==44):
                self.color = (0,0,255)
            elif(drum_hit==46):
                self.color = (0,255,255)
            elif(drum_hit==85):
                self.color = (255,255,0)
            elif(drum_hit==86):
                self.color = (255,0,255)
        elif(drum_hit in [55, 49, 59]):
            #cymbal crash
            if(drum_hit==49):
                self.color = (0,255,0)
            elif(drum_hit==55):
                self.color = (0,0,255)
            else:
                self.color = (0,255,255)
            self.row=1
        elif(drum_hit in [53, 52, 51]):
            #ride
            if(drum_hit==51):
                self.color = (0,255,0)
            elif(drum_hit==52):
                self.color = (0,0,255)
            else:
                self.color = (0,255,255)
            self.row=2
        elif(drum_hit in [37, 38, 40]):
            #snare
            if(drum_hit==37):
                self.color = (0,255,0)
            elif(drum_hit==38):
                self.color = (0,0,255)
            else:
                self.color = (0,255,255)
            self.row=3
        elif(drum_hit == 48):
            #tom_1
            self.color = (0,255,0)
            self.row=4
        elif(drum_hit == 47):
            #tom_2
            self.color = (0,0,255)
            self.row=5
        elif(drum_hit == 43):
            #floor_tom
            self.color = (0,0,0)
            self.row = 6


    def next_frame(self, pixels, t):
        pixels[self.column_location, self.row] = self.color
        self.column_location = self.column_location-1

    def is_completed(self, t):
        return self.column_location < 0 

class DrawA_B(Effect):
    def __init__(self, drum_hit):
        self.color=(255,255,255)
        self.col = STATE.layout.rows-1
        self.b = [
            [0,0],[1,0],[2,0],
            [0,1],[3,1],
            [0,2],[3,2],
            [0,3],[1,3],[2,3],
            [0,4],[1,4],[2,4],
            [0,5],[3,5],
            [0,6],[3,6],
            [0,7],[1,7],[2,7] 
        ]

    def next_frame(self, pixels, t):
        for point in self.b:
            pixels[self.col-point[0],point[1]]=self.color
#        pixels[self.b]=self.color
        self.col -= 1


    def is_completed(self, t):
        return self.col < 0 

class MidiListener(MultiEffect):
    def before_rendering(self, pixels, t):
        super(MidiListener, self).before_rendering(pixels, t)
        for data in STATE.osc_data.current['midi']:
            #self.add_effect(MovingColor(data,slice(0,None)))
            #self.add_effect(DrumHitRow(data))
            if(data.note==36):
                self.add_effect(DrawA_B(data))
            else:
                self.add_effect(DrumHitRow(data))

SCENES = [
    #Scene(
    #    "movingslice",
    #    effects=[MovingSlice()]
    #),
    Scene(
        "solidwhite",
        effects=[
            SolidBackground(color=(150,0,0)),
            MidiListener()
        ]
    ),

]
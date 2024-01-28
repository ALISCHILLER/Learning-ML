#=======================================================================
# stddraw.py
# The stddraw module defines functions that allow the user to create a
# drawing.  A drawing appears on the surface.  The surface appears
# in the window.  As a convenience, the module also imports the
# commonly used Color objects defined in the color module.
#=======================================================================
import time
import os
import sys
import pygame
import pygame.gfxdraw
import pygame.font
import color
import string

#-----------------------------------------------------------------------
# Define colors so clients need not import the color module.
from color import WHITE
from color import BLACK
from color import RED
from color import GREEN
from color import BLUE
from color import CYAN
from color import MAGENTA
from color import YELLOW
from color import DARK_RED
from color import DARK_GREEN
from color import DARK_BLUE
from color import GRAY
from color import DARK_GRAY
from color import LIGHT_GRAY
from color import ORANGE
from color import VIOLET
from color import PINK
from color import BOOK_BLUE
from color import BOOK_LIGHT_BLUE
from color import BOOK_RED

#-----------------------------------------------------------------------
# Return a Pygame Color Object of Color c
def _pygameColor(c):
    """
    Convert c, an object of type color.Color, to an equivalent object
    of type pygame.Color.  Return the result.
    """
    r = c.getRed()
    g = c.getGreen()
    b = c.getBlue()
    return pygame.Color(r, g, b)

#-----------------------------------------------------------------------
# Default Sizes and Values
_BORDER = 0
_DEFAULT_XMIN = 0.0
_DEFAULT_XMAX = 1.0
_DEFAULT_YMIN = 0.0
_DEFAULT_YMAX = 1.0
_DEFAULT_SIZE = 512
_DEFAULT_PEN_RADIUS = .002
_DEFAULT_PEN_COLOR = color.BLACK

_DEFAULT_FONT_FAMILY = 'Helvetica'
_DEFAULT_FONT_SIZE = 12

_xmin = None
_ymin = None
_xmax = None
_ymax = None

_fontFamily = _DEFAULT_FONT_FAMILY
_fontSize = _DEFAULT_FONT_SIZE

_width = _DEFAULT_SIZE
_height = _DEFAULT_SIZE
_penRadius = None
_penColor = _DEFAULT_PEN_COLOR
_keysTyped = []

#top left corner of button is( _buttonLeft, _buttonTop))
_buttonLeft = 10
_buttonTop = 10
_barPadding = 50
#the save button's dimensions are 49 x 30
_buttonWidth = 49
_buttonHeight = 30

#-----------------------------------------------------------------------
# Private functions to scale and factor X and Y values
def _scaleX(x):
    return _width * (x - _xmin) / (_xmax - _xmin)

def _scaleY(y):
    return _height * (_ymax - y) / (_ymax - _ymin)

def _factorX(w):
    return w * _width / abs(_xmax - _xmin)

def _factorY(h):
    return h * _height / abs(_ymax - _ymin)

#-----------------------------------------------------------------------
# Private functions for Save Button and the button's background
def _checkButtonX(mousePoints):
    """Return True if mouse's X coordinate is on the Button"""
    return (mousePoints[0] > _buttonLeft and \
        mousePoints[0] < _buttonLeft + _buttonWidth)

def _checkButtonY(mousePoints):
    """Return True if mouse's Y coordinate is on the Button"""
    return (mousePoints[1] > _buttonTop and \
        mousePoints[1] < _buttonTop + _buttonHeight)

def _checkButton():
    """
    Check if the mouse has clicked on the button.
    """
    global button
    mousePoints = pygame.mouse.get_pos()
    if (_checkButtonX(mousePoints) and \
        _checkButtonY(mousePoints)):
        return True

def _display_buttonBackground(_background, pressed):
    global button
    global buttonBackground
    #initialize font
    pygame.font.init()
    fontobject = pygame.font.Font(None, 18)

    #create buttonBackground surface and load the button image
    buttonBackground = pygame.Surface((_width, _barPadding))
    buttonBackground.fill(_pygameColor(RED))
    button = pygame.image.load(os.path.join( 'saveIcon.png'))
    #check to see if the button is pressed
    if pressed:
        button.fill(_pygameColor(WHITE))

    pygame.draw.line(buttonBackground,
        _pygameColor(BLACK),
        (0, 49),
        (_width - 1, 49))

    buttonBackground.blit(button, (_buttonLeft, _buttonTop))
    _background.blit(buttonBackground, (0, 0))
    pygame.display.flip()
    if pressed:
        pygame.time.wait(150)
    return buttonBackground


#-----------------------------------------------------------------------
def createWindow(w=_DEFAULT_SIZE, h=_DEFAULT_SIZE):
    """
    Create the stddraw window.
    """
    global _background
    global _surface
    global _width
    global _height
    if (w < 1) or (h < 1):
        raise Exception('width and height must be positive')
    _width = w
    _height = h
    _background = pygame.display.set_mode([w, h + _barPadding])
    pygame.display.set_caption('stddraw window')
    _surface = pygame.Surface((w, h))
    _surface.fill(_pygameColor(WHITE))
    #do I need to blit the surface back to the background?
    _display_buttonBackground(_background, False)
    clear()

def setXscale(min=_DEFAULT_XMIN, max=_DEFAULT_XMAX):
    """
    Set the x-scale of the surface such that the minimum x value is
    min and the maximum x value is max.
    """
    global _xmin
    global _xmax
    size = max - min
    _xmin = min - _BORDER * size
    _xmax = max + _BORDER * size

def setYscale(min=_DEFAULT_YMIN, max=_DEFAULT_YMAX):
    """
    Set the y-scale of the surface such that the minimum y value is
    min and the maximum y value is max.
    """
    global _ymin
    global _ymax
    size = max - min
    _ymin = min - _BORDER * size
    _ymax = max + _BORDER * size

def setPenRadius(r=_DEFAULT_PEN_RADIUS):
    """
    Set the pen radius to r.
    """
    global _penRadius
    if r < 0:
        raise Exception('Argument to setPenRadius() must be non-neg')
    _penRadius = r * _DEFAULT_SIZE

def setPenColor(c=_DEFAULT_PEN_COLOR):
    """
    Set the pen color to c, where c is an object of class color.Color.
    """
    global _penColor
    _penColor = c

def setFontFamily(f=_DEFAULT_FONT_FAMILY):
    """
    Set the font family to f (e.g. 'Helvetica' or 'Courier').
    """
    global _fontFamily
    _fontFamily = f

def setFontSize(s=_DEFAULT_FONT_SIZE):
    """
    Set the font size to s (e.g. 12 or 16).
    """
    global _fontSize
    _fontSize = s

#-----------------------------------------------------------------------
# Functions to draw shapes, text, and images on Surface
def _pixel(x, y):
    """
    Draw on the surface a pixel at (x, y).
    """
    xs = _scaleX(x)
    xy = _scaleY(y)

    pygame.gfxdraw.pixel(_surface,
        int(round(xs)),
        int(round(xy)),
        _pygameColor(_penColor))

def point(x, y):
    """
    Draw on the surface a point at (x, y).
    """
    r = _penRadius
    #If the radius is too small, then simply draw a pixel
    if r <= 1:
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)

        pygame.draw.ellipse(_surface,
            _pygameColor(_penColor),
            pygame.Rect(
                int(round(xs-_penRadius)),
                int(round(ys-_penRadius)),
                int(round(_penRadius*2)),
                int(round(_penRadius*2))),
            0)

def line(x0, y0, x1, y1):
    """
    Draw on the surface a line from (x0, y0) to (x1, y1).
    """
    x0s = _scaleX(x0)
    y0s = _scaleY(y0)
    x1s = _scaleX(x1)
    y1s = _scaleY(y1)
    lineWidth = _penRadius * 2.0
    if lineWidth == 0: lineWidth = 1
    pygame.draw.line(_surface,
        _pygameColor(_penColor),
        (int(round(x0s)), int(round(y0s))),
        (int(round(x1s)), int(round(y1s))),
        int(round(lineWidth)))

    # If the line is thick, then round off the endpoints.
    if lineWidth >= 3:
        point(x0, y0)
        point(x1, y1)

def circle(x, y, r):
    """
    Draw on the surface a circle of radius r centered on (x, y).
    """
    ws = _factorX(2*r)
    hs = _factorY(2*r)
    #If the radius is too small, then simply draw a pixel
    if (ws <= 1) and (hs <= 1):
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.ellipse(_surface,
            _pygameColor(_penColor),
            pygame.Rect(int(round(xs-ws/2)),
                int(round(ys-hs/2)), 
                int(round(ws)),
                int(round(hs))),
            int(round(_penRadius)))

def filledCircle(x, y, r):
    """
    Draw on the surface a filled circle of radius r centered on (x, y).
    """
    ws = _factorX(2*r)
    hs = _factorY(2*r)
    #If the radius is too small, then simply draw a pixel
    if (ws <= 1) and (hs <= 1):
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.ellipse(_surface,
            _pygameColor(_penColor),
            pygame.Rect(int(round(xs-ws/2)),
                int(round(ys-hs/2)),
                int(round(ws)),
                int(round(hs))),
            0)

def rectangle(x, y, w, h):
    """
    Draw on the surface a rectangle of width w and height h, centered
    on (x, y).
    """
    global _surface
    ws = _factorX(w)
    hs = _factorY(h)
    #If the rectangle is too small, then simply draw a pixel
    if (ws <= 1) and (hs <= 1):
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.rect(_surface,
            _pygameColor(_penColor),
            pygame.Rect(int(round(xs-ws/2)),
                int(round(ys-hs/2)),
                int(round(ws)),
                int(round(hs))),
            int(round(_penRadius)))

def filledRectangle(x, y, w, h):
    """
    Draw on the surface a filled rectangle of width w and height h,
    centered on (x, y).
    """
    global _surface
    ws = _factorX(w)
    hs = _factorY(h)
    #If the rectangle is too small, then simply draw a pixel
    if (ws <= 1) and (hs <= 1):
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.rect(_surface,
            _pygameColor(_penColor),
            pygame.Rect(int(round(xs-ws/2)),
                int(round(ys-hs/2)),
                int(round(ws)),
                int(round(hs))),
            0)

def square(x, y, r):
    """
    Draw on the surface a square whose sides are of length 2r, centered
    on (x, y).
    """
    rectangle(x, y, 2*r, 2*r)

def filledSquare(x, y, r):
    """
    Draw on the surface a filled square whose sides are of length 2r,
    centered on (x, y).
    """
    filledRectangle(x, y, 2*r, 2*r)

def polygon(x, y):
    """
    Draw on the surface a polygon with coordinates (x[i], y[i]).
    """
    global _surface
    #scale X and Y values
    xScaled = []
    for xi in x:
        xScaled += [_scaleX(xi)]
    yScaled = []
    for yi in y:
        yScaled += [_scaleY(yi)]
    points = []
    for i in range(len(x)):
        points += [(int(round(xScaled[i])), int(round(yScaled[i])))]
    points += [(int(round(xScaled[0])), int(round(yScaled[0])))]
    pygame.draw.polygon(_surface,
        _pygameColor(_penColor),
        points,
        int(round(_penRadius)))

def filledPolygon(x, y):
    """
    Draw on the surface a filled polygon with coordinates (x[i], y[i]).
    """
    global _surface
    #scale X and Y values
    xScaled = []
    for xi in x:
        xScaled += [_scaleX(xi)]
    yScaled = []
    for yi in y:
        yScaled += [_scaleY(yi)]
    points = []
    for i in range(len(x)):
        points += [(int(round(xScaled[i])), int(round(yScaled[i])))]
    points += [(int(round(xScaled[0])), int(round(yScaled[0])))]
    pygame.draw.polygon(_surface, _pygameColor(_penColor), points, 0)

def text(x, y, s):
    """
    Draw on the surface string s centered at (x, y).
    """
    xs = _scaleX(x)
    ys = _scaleY(y)
    font = pygame.font.SysFont(_fontFamily, _fontSize)
    text = font.render(s, 1, _pygameColor(_penColor))
    textpos = text.get_rect(center=(int(round(xs)), int(round(ys))))
    _surface.blit(text, textpos)

def picture(pic, x=None, y=None):
    """
    Draw pic on the surface centered on (x, y).  pic is an object of
    class picture.Picture.
    """
    global _surface
    # By default, draw pic at the middle of the surface.
    if x == None:
        x = (_xmax + _xmin) / 2
    if y == None:
        y = (_ymax + _ymin) / 2
    xs = _scaleX(x)
    ys = _scaleY(y)
    ws = pic.width()
    hs = pic.height()
    picSurface = pic._surface # violates encapsulation
    _surface.blit(picSurface, 
        [int(round(xs-ws/2)),
            int(round(ys-hs/2)),
            int(round(ws)),
            int(round(hs))])

def clear():
    """
    Clear the surface.
    """
    _surface.fill(_pygameColor(WHITE))

def save(f):
    """
    Save the surface to file f.
    """
    pygame.image.save(_surface, f)

#-----------------------------------------------------------------------

def sleep(t):
    """
    Sleep for t milliseconds.
    """
    time.sleep(float(t) / 1000.0)

def show():
    """
    Show the surface on the window.
    """
    _background.blit(_surface, (0, _barPadding))
    pygame.display.flip()
    _checkForEvents()

def wait():
    """
    Wait for the user to close the window.
    """
    while True:
        _checkForEvents()

def _checkForEvents():
    """
    Check if any new event has occured (such as a key typed or button
    pressed).  If a key has been typed, then put that key in a queue.
    """
    global _surface
    global buttonBackground
    global _keysTyped
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            _keysTyped = [event.unicode] + _keysTyped
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if _checkButton():
                _display_buttonBackground(_background,
                    True)
        elif event.type == pygame.MOUSEBUTTONUP:
            if _checkButton():
                import subprocess
                childProcess = subprocess.Popen(
                    ['python', 'dialogboxfile.py'],
                    stdout=subprocess.PIPE)
                so, se = childProcess.communicate()
                fileName = so.rstrip()
                if fileName != '':
                    if fileName.endswith(('.jpg', '.png')):
                        save(fileName)
                        childProcess = subprocess.Popen(
                            ['python', 'dialogboxconfirm.py'])
                    else:
                        childProcess = subprocess.Popen(
                            ['python', 'dialogboxerror.py'])

        _display_buttonBackground(_background, False)
#-----------------------------------------------------------------------
# Functions for retrieving keys
def hasNextKeyTyped():
    """
    Return True iff the queue of keys the user typed is not empty.
    """
    global _keysTyped
    return _keysTyped != []

def nextKeyTyped():
    """
    Remove the first key from the queue of keys that the the user typed,
    and return that key.
    """
    global _keysTyped
    return _keysTyped.pop()

#-----------------------------------------------------------------------
# Initialize the x scale, the y scale, and the pen radius.
setXscale()
setYscale()
setPenRadius()
#-----------------------------------------------------------------------
# For Regression Testing
def _main():
    """
    For testing.
    """

    createWindow()

    clear()
    show()

    setPenRadius(.5)
    setPenColor(ORANGE)
    point(0.5, 0.5)
    show()

    setPenRadius(.25)
    setPenColor(BLUE)
    point(0.5, 0.5)
    show()

    setPenRadius(.02)
    setPenColor(RED)
    point(0.25, 0.25)
    show()

    setPenRadius(.01)
    setPenColor(GREEN)
    point(0.25, 0.25)
    show()

    setPenRadius(0)
    setPenColor(BLACK)
    point(0.25, 0.25)
    show()
    
    setPenRadius(.1)
    setPenColor(RED)
    point(0.75, 0.75)
    show()

    setPenRadius(0)
    setPenColor(CYAN)
    for i in range(0, 100):
        point(i / 512.0, .5)
        point(.5, i / 512.0)
    show()

    setPenRadius(0)
    setPenColor(MAGENTA)
    line(.1, .1, .3, .3)
    line(.1, .2, .3, .2)
    line(.2, .1, .2, .3)
    show()

    setPenRadius(.05)
    setPenColor(MAGENTA)
    line(.7, .5, .8, .9)
    show()
    
    setPenRadius(.01)
    setPenColor(YELLOW)
    circle(.75, .25, .2)
    show()

    setPenRadius(.01)
    setPenColor(YELLOW)
    filledCircle(.75, .25, .1)
    show()

    setPenRadius(.01)
    setPenColor(PINK)
    rectangle(.25, .75, .1, .2)
    show()

    setPenRadius(.01)
    setPenColor(PINK)
    filledRectangle(.25, .75, .05, .1)
    show()

    setPenRadius(.01)
    setPenColor(DARK_RED)
    square(.5, .5, .1)
    show()

    setPenRadius(.01)
    setPenColor(DARK_RED)
    filledSquare(.5, .5, .05)
    show()

    setPenRadius(.01)
    setPenColor(DARK_BLUE)
    polygon([.4, .5, .6], [.7, .8, .7])
    show()

    setPenRadius(.01)
    setPenColor(DARK_GREEN)
    setFontSize(24)
    text(.2, .4, 'hello, world')
    show()

    import picture as p
    pic = p.Picture()
    pic.load('saveIcon.png')
    picture(pic, .5, .85)
    show()

    wait()
if __name__ == '__main__':
    _main()

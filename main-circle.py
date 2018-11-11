#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

from numpy import pi
from numpy import array
from numpy.random import random
from numpy.random import randint

from numpy import linspace
from numpy import arange
from numpy import column_stack
from numpy import cos
from numpy import sin

BG = [1,1,1,1] #background
FRONT = [0,0.4,0.5,0.0005] #colour

TWOPI = 2.0*pi

SIZE = 2500 #size of image

INUM = 2000 #?

GAMMA = 1.5 #?

STP = 0.0000001 #chaos factor

RANDSTART = 0.395 #start width
RANDEND = 0.4 #end width

DISTORTLOW = 10
DISTORTHIGH = 50

def f(x, y):
  while True:
    yield array([[x,y]])

def spline_iterator():
  from modules.sandSpline import SandSpline

  splines = []
  for _ in range(5): # number of circles
    guide = f(0.5,0.5) # centre
    pnum = randint(DISTORTLOW,DISTORTHIGH) #weighted equally
    pnum = math.floor(abs(random() - random()) * (1 + DISTORTHIGH - DISTORTLOW) + DISTORTLOW) #weighted to low end

    a = random()*TWOPI + linspace(0, TWOPI, pnum)
    # a = linspace(0, TWOPI, pnum)

    modifier = ((random()*(RANDEND-RANDSTART))+RANDSTART) #path radius
    path = column_stack((cos(a), sin(a))) * modifier

    scale = arange(pnum).astype('float')*STP

    s = SandSpline(
        guide,
        path,
        INUM,
        scale
        )
    splines.append(s)

  itt = 0
  while True:
    for w, s in enumerate(splines):
      xy = next(s)
      itt += 1
      yield itt, w, xy


def main():
  import sys, traceback
  from fn import Fn
  from sand import Sand
  from modules.helpers import get_colors

  sand = Sand(SIZE)
  sand.set_bg(BG)
  sand.set_rgba(FRONT)

  # colors = get_colors('../colors/colourspectrum.jpg')
  # nc = len(colors)

  fn = Fn(prefix='./res/', postfix='.png')
  si = spline_iterator()

  while True:
    try:
      itt, w, xy = next(si)
      # rgba = colors[w%nc] + [0.0005]
      # sand.set_rgba(rgba)
      sand.paint_dots(xy)
      # if not itt%(20000):
      #   print(itt)
      if not itt%(40000):
        print(itt)
        sand.write_to_png(fn.name(), GAMMA)
    except Exception as e:
      print(e)
      sand.write_to_png(fn.name(), GAMMA)
      traceback.print_exc(file=sys.stdout)


if __name__ == '__main__':
  main()

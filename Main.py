#!/usr/bin/env python

import math
import tkinter as tk
from Graphic import GUI
from GA import GA
from random import *
import time

DELAY = 0.03
DEMO = True

def runGA(demo = False):
   '''
   test code for genetic algo
   :return:
   '''

   gui = GUI(tk.Tk())

   seed()
   ga = GA()

   p = ga.pop(20)
   p = ga.selection(p)
   p = ga.propagate_gen(p)

   t = time.time()

   count = 0
   exptime = 10000
   while (count <= exptime):
      if(GA.getFitness(p) > 0.025):
         p = ga.selection(p)
         p = ga.propagate_gen(p)
         count += 1
         if(demo):
            gui.display_individual(GA.convertPolygon(ga.best_polygon))
            time.sleep(DELAY)
      else:
         if(not demo):
            break

   return [ (time.time() - t), count]


def main():
   if(DEMO):
      runGA(True)

   else:
      avg = 0.0
      run = 100
      for i in range(0, run):
         res = runGA(False)
         timeSpent = res[0] + res[1] * DELAY
         avg += timeSpent
         print(timeSpent)
      print("average", avg/run)

main()

#!/usr/bin/env python
import sys
from argparse import ArgumentParser

import math
import tkinter as tk
from Graphic import GUI
from GA import GA
from random import *
import time

DELAY = 0.01
DEMO = True

def runGA(verts, population, demo = False):
   '''
   test code for genetic algo
   :return:
   '''

   gui = GUI(tk.Tk())

   seed()
   ga = GA(verts=verts)

   p = ga.pop(100)
   p = ga.selection(p)
   p = ga.propagate_gen(p)

   t = time.time()

   count = 0
   exptime = 10000
   while (count <= exptime):
      if(ga.best_polygon[len(ga.best_polygon)-1] > .01):
         #print(count)
         p = ga.selection(p)
         p = ga.propagate_gen(p)
         count += 1
         #print(ga.convertPolygon(ga.best_polygon))
         if(DEMO):
            gui.display_individual(ga.convertPolygon(ga.best_polygon), count)
            time.sleep(DELAY)
      else:
         if not DEMO:
            break

   return [ (time.time() - t), count, ga.best_fitness]


def main(verts=3, population=10):
   if(DEMO):
      runGA(verts, population, True)

   else:
      avgTime = 0.0
      avgError = 0.0
      run = 10
      SIG = 15
      for i in range(0, run):
         res = runGA(False)
         timeSpent = res[0] + res[1] * DELAY
         avgTime += timeSpent
         avgError += res[2]*100.0
         print("time spent(s):", round(timeSpent, 5))
         print("error:", round(res[2]*100.0*1000000, SIG), "%*10^-6")
      print("average time(s):", round(avgTime/run, 5))
      print("average error:", round(avgError/run, SIG), "%")


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-v", "--verts", dest="verts", type=int,
                        help="How many vertices should each generation run")
    parser.add_argument("-p", "--population", dest="population", type=int,
                        help="What population should each generation contain")

    args = vars(parser.parse_args())
    main(verts=args['verts'], population=args['population'])

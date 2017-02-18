#!/usr/bin/env python

from random import *
from copy import deepcopy
from operator import itemgetter

class GA:
   RADIUS = 1
   DEG_SIG = 5
   DO_MUTATE = False
   MUTATION_RATE = .1  # rate in which pop will be mutated
   MUTATION_AMT = 5  # +/- random range for mutation
   BAD_SAMPLE_RATE = 0.1

   def __init__(self):
      self.gen_count = 1
      self.current_gen = []
      self.best_polygon = []
      self.best_fitness = 0

   @staticmethod
   def convertFitPolygon(simplyPolygon):
      return [ [simplyPolygon[0], GA.RADIUS],
               [simplyPolygon[1], GA.RADIUS],
               [simplyPolygon[2], GA.RADIUS] ]

   def polygon(self):
      '''
      returns a list with a series of three theta radius pairs
      :return: list[ [0,R], [0,R], [0,R]
      '''
      cir = 360.0
      rand_angles = GA.gen_pairs(cir)
      formattedRandAngles = GA.convertFitPolygon(rand_angles)
      while(rand_angles[0] == rand_angles[1] or
            rand_angles[0] == rand_angles[2] or
            rand_angles[1] == rand_angles[2] or
            self.fitness(formattedRandAngles) < self.BAD_SAMPLE_RATE):
         rand_angles = GA.gen_pairs(cir)
         formattedRandAngles = GA.convertFitPolygon(rand_angles)

      vertz = []
      for i in range(0, len(rand_angles)):
         vertz.append([rand_angles[i],self.RADIUS])
      return vertz

   @staticmethod
   def gen_pairs(angle):
      pairs = [uniform(0, angle), uniform(0, angle), uniform(0, angle)]
      for i in range(0, len(pairs)):
         pairs[i] = round(pairs[i],GA.DEG_SIG)
      pairs.sort()
      return pairs

   def pop(self, size):
      '''
      returns a set of N polygons
      :param size: integer
      :return: list[n polygons...]
      '''
      return [self.polygon() for x in range(size)]

   @staticmethod
   def fitness(polygon):
      '''
      returns a fitness for an polygon
      :param polygon:
      :return:
      '''
      thetaA = polygon[0][0]+(360-polygon[2][0])
      thetaB = polygon[1][0] - polygon[0][0]
      thetaC = polygon[2][0] - polygon[1][0]

      thetaA = abs(thetaA - 120)
      thetaB = abs(thetaB - 120)
      thetaC = abs(thetaC - 120)
      '''
      thetaA = 120 - abs(polygon[0][0] - polygon[2][0])
      thetaB = 120 - abs(polygon[1][0] - polygon[0][0])
      thetaC = 120 - abs(polygon[2][0] - polygon[1][0])
      '''
      sum = thetaA + thetaB + thetaC
      return round(abs(sum/360.0), 3)


   def selection(self, pop):
      '''
      appends a fitness value for each polygon
      :return:
      '''
      numElem = len(pop)
      for i in range(0, numElem):
         fitVal = self.fitness(pop[i])
         pop[i] = [pop[i][0], pop[i][1], pop[i][2], fitVal]

      '''
      print("selection:pop:")
      for p in pop:
         print(p)
      print("End---")
      '''
      return sorted(pop, key = itemgetter(3))

   def propagate_gen(self, pop):
      '''
      preforms selection on current gen.
      keeps best and splices the rest
      :param pop:
      :return:
      '''
      new_pop = deepcopy(pop)
      for i in range(1, len(pop)):
         new_pop[i] = self.splice_polygon(pop[i-1], pop[i])
         new_pop = GA.sortByFitness(new_pop)
      if self.DO_MUTATE:
         self.mutation(new_pop)
      self.current_gen = new_pop
      self.best_polygon = new_pop[0]
      self.best_fitness = new_pop[0][len(new_pop[0]) - 1]
      return new_pop

   @staticmethod
   def splice_polygon(polygonA, polygonB):
      new_polygon = deepcopy(polygonA)
      pairs_len = len(new_polygon) - 1
      setA = set()
      for i in range(0, pairs_len):
         setA.add(i)
      index = sample(setA, pairs_len)
      # needs to be dynamic
      count = int(len(new_polygon)/2) # 3
      for i in range(0, pairs_len - count):
         new_polygon[i][0] = polygonA[index[i]][0]
      for i in range(0, count):
         new_polygon[i][0] = polygonB[index[i]][0]
      # sorts pairs and recomputes fitness
      GA.sortPairs(new_polygon)
      new_polygon[pairs_len] = GA.fitness(new_polygon)
      return new_polygon

   @staticmethod
   def getKey(item):
      return item[0]

   @staticmethod
   def getFitness(gen):
      return gen[0][3]

   @staticmethod
   def sortByFitness(gen):
      return sorted(gen, key = itemgetter(3))

   @staticmethod
   def sortPairs(polygon):
      pairs = []
      pairs_len = len(polygon) - 1
      for i in range(0, pairs_len):
         pairs.append(polygon[i])
      pairs = sorted(pairs)
      for i in range(0, pairs_len):
         polygon[i] = pairs[i]
      return polygon

   @staticmethod
   def convertPolygon(polygon):
      return [[polygon[0], polygon[1], polygon[2]], polygon[3]]

   def mutation(self, gen):
      infect_rate = uniform(0,self.MUTATION_RATE)
      for i in range(0, int(infect_rate* len(gen)) ):
         index = randrange(0, len(gen))
         self.infect(gen[index])


   def infect(self, polygon):
      pairs_len = len(polygon) - 1
      for i in range (0, pairs_len):
         index = randrange(0, pairs_len)
         polygon[index][0] += randint(-self.MUTATION_AMT, self.MUTATION_AMT)
         if polygon[index][0] >= 360:
            polygon[index][0] -= 360
         elif polygon[index][0] < 0:
            polygon[index][0] += 360
      return GA.sortPairs(polygon)


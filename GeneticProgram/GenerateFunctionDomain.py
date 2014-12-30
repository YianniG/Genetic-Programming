'''
Created on 23 Dec 2014

@author: Ioannis
'''
from operator import contains
from random import Random

class GenerateFunctionDomain(object):


    valueRange = [];
    bannedValues = [];

    onlyIntegers = False;
    useBanned = False;
    useRange = False;

    rand = Random();

    def __init__(self, vrange = [], bannedValues = [], onlyIntegers = False):
        self.valueRange = vrange;
        self.bannedValues = bannedValues;
        self.onlyIntegers = onlyIntegers;

    def getRandomValue(self):

        if (len(self.valueRange) > 0):
            # range is in use
            self.useRange = True;
        if (len(self.bannedValues) > 0):
            # banned is in use
            self.useBanned = True;

        return self.doWork();

    def doWork(self):
        if (self.useRange and self.onlyIntegers):
            value = self.rand.randrange(self.valueRange[0], self.valueRange[1])

        if (self.useRange):  # Not just integers
            value = self.rand.random() + self.rand.randint(self.valueRange[0], self.valueRange[1] - 1);

        if (contains(self.bannedValues, value)):
            return self.doWork();
        return value;
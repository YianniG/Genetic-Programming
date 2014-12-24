'''
Created on 5 Oct 2014

@author: Ioannis
'''

from random import Random;
from math import ceil;
import math;
from GP.GenerateFunctionDomain import GenerateFunctionDomain

mistakes = [];

def addFunction(a):
    if(not isinstance(a, list) and not isinstance(a[0], float) and not isinstance(a[1], float)):
        mistakes.append(str(["Error add: ", a]));
        return float(1);
    return float(a[0])+float(a[1]);

def mulitplyFunction(a):
    if(not isinstance(a, list) and not isinstance(a[0], float) and not isinstance(a[1], float)):
        mistakes.append(str(["Error mult: ", a]));
        return float(1);
    return float(a[0])*float(a[1]);

def divideFunction(a):
    if(not isinstance(a, list) and not isinstance(a[0], float) and not isinstance(a[1], float)):
        mistakes.append(str(["Error div: ", a]));
        return float(1);
    if(a[1]==0):
        return float(0);
    return float(a[0])/float(a[1]);

def powerFunction(a):
    if(not isinstance(a, list) and not isinstance(a[0], float)):
        mistakes.append(str(["Error pow: ", a]));
        return float(1);
    if(a[0]<=0 and a[1]%1>0):
        return 0;
    if(a[1]>1.0e+1 or a[1]<1.0e-2 or a[0]>=1.0e+10): #Have to cap it off at some point.
        return 1;
    return math.pow(float(a[0]),float(a[1]));

def factorialFunction(a):
    if(isinstance(a, list)):
        b=a[0];
    else:
        b=a;
    if(b<=0):
        return float(1);
    elif(b>170):
        return 1;
    if(not b%1==0):
        mistakes.append(str(["Error fact rounding: ", b]));
    hold = int(b);
    return hold*factorialFunction(hold-1); 
    
    
functions = ["+", "*", "/","!", "^", ];
functionImportance = {"+":1, "*":2, "/":3, "^":4, "!":5,};
functionArgNumber = {"+":2,
                     "*":2,
                     "/":2,
                     "!":1,
                     "^":2,
                      };
functionMap = {"+": addFunction,
                "*": mulitplyFunction,
                "/": divideFunction,
                "!": factorialFunction,
                "^": powerFunction,
                };
                            
functionDomain = {"+":GenerateFunctionDomain([-5,5], [], False), "*":GenerateFunctionDomain([-5,5], [], False), "/":GenerateFunctionDomain([-5,5], [0], False), "^":GenerateFunctionDomain([0,5], [], False), "!":GenerateFunctionDomain([0,5], [], True)};
aim = 25;
maxPrograms = 1000;
topPercentage = 0.2;    #top percentage of the fit, that continue
randMaker = Random();
#Create tree
trees = [];
maxLines = 25;

treeFitness = {};
successTrees = {};

def createTree(a, prevFunction = None):
    if(a==0):
        fun = functions[int(randMaker.randint(0, len(functions)-1))];
        sub = [fun];
        args = functionArgNumber[fun];
        for c in range(0, args):
            sub.append(createTree(a+1));
        return sub;
    elif(a==maxLines):
        #Too busy
        if(prevFunction == None):
            return 1; #Easy way out.
        return functionDomain[prevFunction].getRandomValue();
    elif(randMaker.random()<0.5):
        #Function
        fun = functions[int(randMaker.randint(0, len(functions)-1))];
        sub = [fun];
        args = functionArgNumber[fun];
        for c in range(0, args):
            sub.append(createTree(a+1, fun));
            c;
        return sub;
    else:
        #Domain
        if(prevFunction == None):
            return 1; #Easy way out.
        return functionDomain[prevFunction].getRandomValue();  

while len(trees)<maxPrograms:
    #Do functions
    trees.append(createTree(0));
    print("Tree #", len(trees)-1, ": ", trees[len(trees)-1]);

#Evaluate trees
def value(tree):
    #evaluate tree
    if(not isinstance(tree, list)):
        return tree;
    if(len(tree)==1):
        return tree[0]; #return value at base of tree
    elif(len(tree)>=2):
        if(tree[0] in functions):
            h = tree[1:functionArgNumber[tree[0]]+1];
            result = [];
            for branch in h:
                result.append(value(branch));
            return functionMap[tree[0]](result);
        else:
            return tree;
    return #number

def countNodes(tree):
    total = 0;
    if(isinstance(tree, list)):
        if(tree[0] in functions):
            numberOfArguments = functionArgNumber[tree[0]];
            for step in range(1,numberOfArguments+1):
                total = total + countNodes(tree[step]) + 1;
    return total;
    
def calcFitness(tree): #Need to include No of rows 
    va = value(tree);
    nodes = countNodes(tree);
    return abs(1-(va/aim))+nodes; #closest to the aim and least amount of nodes.
    
for count in range(0, len(trees)):
    fitness = calcFitness(trees[count]);
    treeFitness[fitness] = count;
    print("Fitness #", count, ": ", fitness);

def quickSort(fitnessValue):
    if len(fitnessValue) <= 1:
        return fitnessValue;
    pivot = int(len(fitnessValue)/2);
    lessThanPivot = [];
    equalToPivot = [];
    moreThanPivot = [];
    for a in fitnessValue:
        if a == fitnessValue[pivot]:
            equalToPivot.append(a);
        elif a<fitnessValue[pivot]:
            lessThanPivot.append(a);
        elif a>fitnessValue[pivot]:
            moreThanPivot.append(a);
    return quickSort(lessThanPivot) + equalToPivot + quickSort(moreThanPivot);

sortedFitnesses = quickSort(list(treeFitness.keys()));

for a in range(0, ceil(len(sortedFitnesses)*topPercentage)):
    successTrees[treeFitness[sortedFitnesses[a]]] = trees[treeFitness[sortedFitnesses[a]]];

print(sortedFitnesses);
print();
print("Top",topPercentage*100,"%:    Aim:", aim); #Break line
if len(successTrees)>0:
    for tree in successTrees:
        print("Successes: #", tree, " ", successTrees[tree]);
else:
    print("No successes");
print();
print("Mistakes: ");
print(mistakes);
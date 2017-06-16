#from externals import *
import SQLQuery

def addNutri(tplL):
 # element-wise sum of 'list of tpl of floats'
 # result is 'tpl of floats'
 listL = [list(itemT) for itemT in tplL]
 result = [sum([listL[i][j] for i in range(len(listL))]) for j in range(len(listL[0]))]
 return result


def foods2nutri(foodL):
 # add up all the nutrients in the given list of foods
 # return a tpl
 return addNutri([nutrientContent(i) for i in foodL])


def findMissingNutri(ingredientL):
 # find the nutrient(s) completely missing from list of ingredients
 # assumes all nutrient contents are nonnegative
 
 # add up all nutrients, nutriSum is a tpl
 nutriSum = addNutri([nutrientContent(item) for item in ingredientL])
 # find zero component(s)
 indices = [i for i in range(len(nutriSum)) if nutriSum[i]==0]
 return indices


def fewestComplete(foodIdL):
 # find the lowest no of ingredients that have all types of nutrients
 # return a 'list of foodIDs' (the first list found)
 from itertools import combinations
 
 # brute force: check if 1,2,.. items are enough
 for num in range(1,len(foodIdL)+1):
  # try all combinations [n choose k of them]
  for foodSubset in combinations(foodIdL,num):
   result = list(foodSubset)
   if findMissingNutri(foods2nutri(result))==[]:
    return result
 return foodIdL


def findMinMass(foodIdL):
 # optimise the mass of the ingredients and find a subset of those
 # that satisfy the recommended daily intake
 # [return subset of foods + amount of each of them + total mass(?)]
 # return a dict of food amounts
 from scipy.optimize import linprog
 
 # access databases
 foodNutritionById = dict([(food, SQLQuery.searchFoodNutritionByID(food)) for food in foodIdL])
 nutritionMinMaxD = SQLQuery.getNutritionMinMax()
 # fix the order of nutrients
 nutriL = [key for key in nutritionMinMaxD]
 
 # check if keys are the same?
 
 # all-ones cost function, ie kinda minimizing mass
 c = [1 for i in range(len(foodIdL))]
 
 # encode min & max daily intake as nutrient constraints
 # min is -a1.x1 <= -b1 (b1 <= a1.x1)
 # max is  A1.x1 <=  B1
 minA = [[-foodNutritionById[food][i] for i in nutriL] for food in foodIdL]
 maxA = [[foodNutritionById[food][i] for i in nutriL] for food in foodIdL]
 
 A_ub = [list(x) for x in zip(*minA)]+[list(x) for x in zip(*maxA)]   # transpose
 
 # lower & upper bounds
 b_ub = [-nutritionMinMaxD[i][0] for i in nutriL] + [nutritionMinMaxD[i][1] for i in nutriL]
 
 # print(c,A_ub,b_ub)
 
 # simplex
 res = linprog(c, A_ub, b_ub, options={"disp": False})
 
 return res.x


def myMain():
 foodL = getFridgeContent()
 # nutrientL = [nutrientContent(food) for food in foodL]
 # nutriSum = addNutri(nutrientL)
 # missingNutri = findMissingNutri(nutriSum)
 foodMassL = findMinMass(foodL)
 print(foodMassL)


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
 # return a dict: status, food amounts
 from scipy.optimize import linprog
 
 # access databases
 foodNutritionById = dict([(food,SQLQuery.searchFoodNutritionByID(food)) for food in foodIdL])
 nutritionMinMaxD = SQLQuery.getNutritionMinMax()
 
 # check if keys are the same
 # if foodNutritionById[].keys() != nutritionMinMaxD.keys():
 #  print("The names of nutrients aren't the same in the 2 DBs! Exit.")
 #  print(.symmetric_difference(nutritionMinMaxD.keys()))
 
 # set the order of nutrients
 nutriL = [key for key in nutritionMinMaxD]
 
 
 ## find missing nutrients
 missingNutri = []
 # add up a unit amount of each ingredient
 # nutriSum: {"fat": 0, "carb": 1}
 nutriSum = {}
 for nutri in nutriL:
  nutriSum[nutri] = 0
 for food in foodIdL:
  for nutri in nutriL:
   nutriSum[nutri] += foodNutritionById[food][nutri]
 # check
 for nutri in nutriL: # name of nutrients
  if nutriSum[nutri] == 0:
   missingNutri.append(nutri)
 if missingNutri != []:
  return {"status": 4, "missing nutrients": missingNutri}
 
 ## optimisation
 
 # all-ones cost function, ie kinda minimizing mass
 c = [1 for i in range(len(foodIdL))]
 
 # encode min & max daily intake as nutrient constraints
 # min is -a1.x1 <= -b1 (b1 <= a1.x1)
 # max is  A1.x1 <=  B1
 minA = [[-foodNutritionById[food][nutri] for nutri in nutriL] for food in foodIdL]
 #maxA = [[foodNutritionById[food][nutri] for nutri in nutriL] for food in foodIdL]
 
 A_ub = [list(x) for x in zip(*minA)]#+[list(x) for x in zip(*maxA)]   # transpose
 
 # lower & upper bounds
 b_ub = [-nutritionMinMaxD[i][0] for i in nutriL] #+ [nutritionMinMaxD[i][1] for i in nutriL]
 
 #print(A_ub)
 #print(b_ub)
 #print(c)
 
 # simplex
 res = linprog(c, A_ub=A_ub, b_ub=b_ub, options={"disp": False})
 
 if res.status==2:
  return {"status": res.status,"missing nutrient names": []}
 
 result = {"status": res.status, "items": [{"id": foodIdL[i],"name":  foodNutritionById[foodIdL[i]]["food_name"], "amount": res.x[i]} for i in range(len(foodIdL))]}
 return result










def myMain():
 foodL = getFridgeContent()
 # nutrientL = [nutrientContent(food) for food in foodL]
 # nutriSum = addNutri(nutrientL)
 # missingNutri = findMissingNutri(nutriSum)
 foodMassL = findMinMass(foodL)
 print(foodMassL)


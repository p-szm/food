#!/usr/bin/python
import sys
import re
import psycopg2
from configparser import ConfigParser
 
 
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db
 
def executeQuery(query, varTuple = None):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        ## print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        conn.set_session(readonly=True)
        # create a cursor
        cur = conn.cursor()
        
 # execute a statement
        # print(query)
        # print(varTuple)
        cur.execute(query, varTuple)
        
        # display the PostgreSQL database server version
        queryrows = cur.fetchall()
        
        # print("The number of parts: " + str(cur.rowcount))
        # for row in queryrows:
        #    print(row)
       
     # close the communication with the PostgreSQL
        conn.commit()
        cur.close()
        return queryrows
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    finally:
        if conn is not None:
            
            conn.close()
            ## print('Database connection closed.')

def executeQueryWithColumns(query, varTuple = None):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        ## print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        conn.set_session(readonly=True)
        # create a cursor
        cur = conn.cursor()
        
 # execute a statement
        # print(query)
        # print(varTuple)
        cur.execute(query, varTuple)
        
        # display the PostgreSQL database server version
        queryrows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        # print("The number of parts: " + str(cur.rowcount))
        # for row in queryrows:
        #    print(row)
        
     # close the communication with the PostgreSQL
        conn.commit()
        cur.close()
        return [zip(colnames, row) for row in queryrows]

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    finally:
        if conn is not None:
            
            conn.close()
            ## print('Database connection closed.')
 
def getFoodNutritionByNameConstraints(foodNameConstraints = "", limit = 5):
    names = foodNameConstraints.split()
    commands = [        
    """
    SELECT Food_ID, Food_Name
    FROM products 
    {0}
    ORDER BY {1}
    {2}
    ;
    """
    ]

    names = ['%' + name + '%' for name in names]
    if names == []:
        constraints = ""
        order_SQL = "Food_Name"
    else:    
        constraints = ("WHERE LOWER(Food_Name) LIKE LOWER(%s)") + ''.join([" AND LOWER(Food_Name) LIKE LOWER(%s)" for i in range(len(names) - 1)])
        order_SQL = "CHAR_LENGTH(Food_Name), Food_Name"
        #print(constraints)
    if limit == 0:
        limit_SQL = ""
    else:
        limit_SQL = "LIMIT " + str(limit) 

    return executeQuery(commands[0].format(constraints, order_SQL, limit_SQL), tuple(names))

def getFoodNutritionByID(foodID):
    query = """
        SELECT *
        FROM products 
        WHERE Food_ID = %s
        ;
        """
    return executeQueryWithColumns(query, tuple([foodID]))

def getMultipleFoodNutritionByID(foodIDListStr):
    foodIDList = foodIDListStr.split(',')
    idConstraints = "( %s" + ''.join([", %s " for i in range(len(foodIDList) - 1)]) + ")"
    query = """
        SELECT *
        FROM products 
        WHERE Food_ID IN {0}
        ;
    """

    return executeQueryWithColumns(query.format(idConstraints), tuple(foodIDList))

def getFoodOrderByHighestNutrition(nutritionsOrders = "", limit = 5):
    nutritions = nutritionsOrders.split()
    commands = [        
    """
    SELECT *
    FROM products 
    ORDER BY {0}
    {1}
    ;
    """
    ]
    if nutritions == []:
        order_SQL = "CHAR_LENGTH(Food_Name), Food_Name"
    else:    
        orders = ''.join(["{0} DESC, ".format(nutrition) for nutrition in nutritions])
        order_SQL = orders + "CHAR_LENGTH(Food_Name), Food_Name"
        #print(constraints)
    if limit == 0:
        limit_SQL = ""
    else:
        limit_SQL = "LIMIT " + str(limit) 

    return executeQueryWithColumns(commands[0].format(order_SQL, limit_SQL), None)

def getFoodOrderByHighestNutritionSum(nutritionsOrders = "", limit = 5):
    nutritions = nutritionsOrders.split()
    commands = [        
    """
    SELECT *
    FROM products 
    ORDER BY {0}
    {1}
    ;
    """
    ]
    if nutritions == []:
        order_SQL = "CHAR_LENGTH(Food_Name), Food_Name"
    else:    
        orderStr = "( " + nutritions[0] + ''.join([" + {0}".format(nutrition) for nutrition in nutritions[1:]]) + " ) DESC,"
        order_SQL = orderStr + "CHAR_LENGTH(Food_Name), Food_Name"
        #print(constraints)
    if limit == 0:
        limit_SQL = ""
    else:
        limit_SQL = "LIMIT " + str(limit) 

    return executeQueryWithColumns(commands[0].format(order_SQL, limit_SQL), None)

def getNutritionMinMax():
    query = """
    SELECT LOWER(name), min_intake, max_intake
    FROM nutrients 
    ;
    """
    rows = executeQuery(query, None)
    if rows is None or len(rows) < 1:
        return {}
    rows = [(x,(y,z)) for (x,y,z) in rows]
    return dict(rows)

def searchFoodByText(searchText):
    if searchText is None:
        rows = getFoodNutritionByNameConstraints("", 20)
    else:
        rows = getFoodNutritionByNameConstraints(searchText, 20)
    if rows is None:
        return {'total_count': 0, 'items': [{'id' : -1, 'name' : "Query Error"}]}
    items = [{'id' : fid, 'name' : fname } for (fid,fname) in rows]
    return {'total_count': len(rows), 'items': items} 

def searchFoodNutritionByID(searchText):
    if searchText is None:
        rows = getFoodNutritionByID("")
    else:
        rows = getFoodNutritionByID(searchText)

    if rows is None or len(rows) < 1:
        return {}
    return dict(rows[0])

def searchMultipleFoodNutritionByID(searchText):
    if searchText is None:
        rows = getMultipleFoodNutritionByID("")
    else:
        rows = getMultipleFoodNutritionByID(searchText)

    if rows is None or len(rows) < 1:
        return {}
    return [dict(row) for row in rows]

def searchFoodOrderByHighestNutrition(nutritions, limit):
    nutritionsSplit = nutritions.split()
    valid = True
    for nutrition in nutritionsSplit:
        if not re.match("^[A-Za-z][0-9A-Za-z_]*$", nutrition):
            print ("Not Valid:" + nutrition)
            valid = False
    return getFoodOrderByHighestNutrition(nutritions, limit)

def searchFoodOrderByHighestNutritionSum(nutritions, limit):
    nutritionsSplit = nutritions.split()
    valid = True
    for nutrition in nutritionsSplit:
        if not re.match("^[A-Za-z][0-9A-Za-z_]*$", nutrition):
            print ("Not Valid:" + nutrition)
            valid = False
    return getFoodOrderByHighestNutritionSum(nutritions, limit)

if __name__ == '__main__':


    if len(sys.argv) > 2:
        querytext = sys.argv[2]
        if sys.argv[1] == "nutri":
            limit_text = sys.argv[3]
            rows = getFoodNutritionByNameConstraints(querytext, int(limit_text))
        elif sys.argv[1] == "fid":
            # rows = getFoodNutritionByID("'" + querytext + "'")
            rows = getFoodNutritionByID(querytext)
        elif sys.argv[1] == "mfid":
            rows = searchMultipleFoodNutritionByID(querytext)
        elif sys.argv[1] == "serverFood":
            rows = None
            print(searchFoodByName(querytext))
        elif sys.argv[1] == "nutSort":
            limit_text = sys.argv[3]
            rows = searchFoodOrderByHighestNutrition(querytext, int(limit_text))
        elif sys.argv[1] == "nutSumSort":
            limit_text = sys.argv[3]
            rows = searchFoodOrderByHighestNutritionSum(querytext, int(limit_text))
        else:
            rows = None
    elif len(sys.argv) > 1:
        if sys.argv[1] == "nutriMinMax":
            print (getNutritionMinMax())
            rows = None
    else:
        rows = getFoodNutritionByNameConstraints("chicken egg", 5)

    if rows is not None:
        print("Number of results: " + str(len(rows)))
        for row in rows[:10]:
            print(row)
    else:
        print("None")
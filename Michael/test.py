#!/usr/bin/python
import psycopg2
from configparser import ConfigParser
 
 
def config(filename='database2.ini', section='postgresql'):
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
 
def executeQuery(query):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        ## print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
 
        # create a cursor
        cur = conn.cursor()
        
 # execute a statement
            
        cur.execute(query)
        
        # display the PostgreSQL database server version
        queryrows = cur.fetchall()
        
        ## print("The number of parts: " + str(cur.rowcount))
        ## for row in queryrows:
        ##    print(row)
       
     # close the communication with the PostgreSQL
        conn.commit()
        cur.close()
        return queryrows
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            
            conn.close()
            ## print('Database connection closed.')

 
def getFoodNutritionByNameConstraints(foodNameConstraints):
    names = foodNameConstraints.split()
    if names == []:
        constraints = ""
        commands = [        
        """
        SELECT *
        FROM nutrients 
        {0}
        ORDER BY Food_Name
        ;
        """
        ]
    else:    
        constraints = ("WHERE LOWER(Food_Name) LIKE LOWER('%{0}%')".format(names[0])) + ''.join([" AND LOWER(Food_Name) LIKE LOWER('%{0}%')".format(name) for name in names[1:]])
        commands = [        
        """
        SELECT *
        FROM nutrients 
        {0}
        ORDER BY CHAR_LENGTH(Food_Name), Food_Name
        ;
        """
        ]
    return executeQuery(commands[0].format(constraints))

def getFoodNutritionByID(foodID):
    query = """
        SELECT *
        FROM nutrients 
        WHERE Food_ID = {0}
        ;
        """
    return executeQuery(query.format(foodID))

if __name__ == '__main__':
    rows = getFoodNutritionByNameConstraints("abc")
    if rows is not None:
        print("Number of results: " + str(len(rows)))
        for row in rows[:5]:
            print(row[2])
    else:
        print("None")
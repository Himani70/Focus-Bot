import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import psycopg2
from config import config
from datetime import date

def getValues(input):
    '''
    :return: Data x,y for dataframe
    TODO : connect to database to extract data and calculations
    '''
    x = np.reshape(input,(-1,8))
    x = np.transpose(x)
    plot(x)
    #x = np.random.random((8,5))
    #return x

def plot(x):
    '''
    :param x: x axis data
    :return: downloads the heatmap as heat-map.png in the same folder for now
    '''
    df = pd.DataFrame(x, columns=["Mon","Tue","Wed","Thu","Fri"])
    ax=sns.heatmap(df,linewidths=1, linecolor='white', cmap="Greens", cbar=True, annot = False, vmin=0, vmax=1)
    bottom, top = ax.get_ylim()

    pos, textvals = plt.yticks()
    plt.yticks(pos, ('8', '7', '6', '5', '4', '3', '2','1'), rotation=0, fontsize="10", va="center")
    plt.ylabel("Sessions")
    ax.set_ylim(bottom , top)
    plt.savefig('heat-map.png')

def showProgressGraph(userId):
    conn = None
    try:
    
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        weekNumber = date.today().strftime("%W")
        #print(weekNumber)
        
        #Does not handle NULL values
        query = "Select cast(session1 as float), cast(session2 as float), cast(session3 as float),cast(session4 as float),cast(session5 as float),cast(session6 as float),cast(session7 as float),cast(session8 as float),cast(session9 as float),cast(session10 as float),cast(session11 as float),cast(session12 as float),cast(session13 as float),cast(session14 as float), cast(session15 as float),cast(session16 as float),cast(session17 as float),cast(session18 as float),cast(session19 as float),cast(session20 as float),cast(session21 as float), cast(session22 as float),cast(session23 as float),cast(session24 as float),cast(session25 as float),cast(session26 as float),cast(session27 as float),cast(session28 as float),cast(session29 as float), cast(session30 as float),cast(session31 as float),cast(session32 as float),cast(session33 as float),cast(session34 as float),cast(session35 as float),cast(session36 as float),cast(session37 as float),cast(session38 as float),cast(session39 as float),cast(session40 as float) from focussession where userid = %s and weekid = %s"

        cur.execute(query,(userId,weekNumber))
        row = cur.fetchall() 

        #print(row)
        
        getValues(row)
      
    except (Exception, psycopg2.Error) as error :
    	print ("Error: ", error)

    finally:
        if conn is not None:
            conn.close() 
 
if __name__ == '__main__':

    userId = 'user2'
    showProgressGraph(userId)

#x= getValues()
#plot(x)

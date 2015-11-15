
# run with:
#
#    python proj-server.py 8080
#
# You can use any legal port number instead of 8080
# of course
#

from bottle import get, post, run, request, static_file, redirect
import os
import sys
import sqlite3

import traceback

from bottle import response
from json import dumps


MORTALITYDB = "mortality.db"


def pullData ():
    conn = sqlite3.connect(MORTALITYDB)
    cur = conn.cursor()

    try: 

        # First Question - Average Age by Cause of Death, Year
        # cur.execute("""SELECT year, Cause_Recode_39, avg(Age_Value), SUM(1) as total 
        #                FROM mortality
        #                GROUP BY year, Cause_Recode_39""")
        # data = [{"year":int(year),
        #          "cause":int(cause),
        #         "avg": int(avg),
        #          ## "gender":sex,
        #          "total":total} for (year, cause, avg, total,) in  cur.fetchall()]
        # conn.close()

        # causes = list(set([int(r["cause"]) for r in data]))

        # cur.execute("""SELECT Cause_Recode_39, Age_Value, Manner_Of_Death,
        #    Method_Of_Disposition, Place_Of_Death, Place_Of_Causal_Injury, Education, SUM(1) as total 
        #                FROM mortality
        #                GROUP BY Age_Value """)
        #                #ORDER by COUNT(Cause_Recode_39) desc 
        #                #limit 85
                      
        # data = [{##"year":int(year),
        #          "cause":int(cause),
        #         "age": int(age),
        #         "manner": str(manner),
        #         "method": str(method),
        #         "place": str(place),
        #         "injury": str(injury),
        #          ## "gender":sex,
        #          "total":total} for (cause, age, manner, method, place, injury, total,) in  cur.fetchall()]
        # conn.close()

        #causes = list(set([int(r["cause"]) for r in data]))

        ##genders = list(set([r["gender"] for r in data]))

        cur.execute("""SELECT year, Cause_Recode_39, Month_Of_Death, SUM(1) as total 
                       FROM mortality
                       GROUP BY year, Cause_Recode_39, Month_Of_Death""")
        data = [{"year":int(year),
                 "cause":int(cause),
                "month": month,
                 ## "gender":sex,
                 "total":total} for (year, cause, month, total,) in  cur.fetchall()]
        conn.close()

        causes = list(set([int(r["cause"]) for r in data]))
        months = list(set([int(r["month"]) for r in data]))

        return {"data":data, 
                ##"genders":genders,
                "causes":causes,
                "months":months
               }

    except: 
        print "ERROR!!!"
        conn.close()
        raise


        
# get all data
    
@get("/data")
def data ():
    return pullData()

    
@get('/<name>')
def static (name="index.html"):
    return static_file(name, root='.')  # os.getcwd())


def main (p):
    run(host='0.0.0.0', port=p)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        print "Usage: server <port>"


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
        cur.execute("""SELECT year, sex, Month_Of_Death, Education, SUM(1) as total 
                       FROM mortality
                       GROUP BY year, Cause_Recode_39, sex""")
        data = [{"year":int(year),
                 "cause":int(cause),
                 "gender":sex,
                 "education": education,
                 "total":total} for (year, cause, sex, month, education, total,) in  cur.fetchall()]
        conn.close()

        genders = list(set([r["gender"] for r in data]))
        months = list(set([int(r["month"]) for r in data]))
        education = list(set([r["education"] for i in data]))

        return {"data":data, 
                "genders":genders,
                "month": month,
                "education": education}

    except: 
        print "ERROR!!!"
        conn.close()
        raise

# First Question - Average Age by Cause of Death, Year
def getAvgAgeFromCause():
    conn = sqlite3.connect(MORTALITYDB)
    cur = conn.cursor()

    try: 
        
        cur.execute("""SELECT year, Cause_Recode_39, avg(Age_Value)
                       FROM mortality
                       GROUP BY year, Cause_Recode_39""")
        data = [{"year":int(year),
                 "cause":int(cause),
                "avg": int(avg)
                } for (year, cause, avg,) in  cur.fetchall()]
        conn.close()

        # causes = list(set([int(r["cause"]) for r in data]))

        return {"data":data}

    except: 
        print "ERROR!!!"
        conn.close()
        raise

# Second Question - Top Cause of death for each age, and each year.
def getMaxCauseForAge():
    conn = sqlite3.connect(MORTALITYDB)
    cur = conn.cursor()
    try: 
        cur.execute("""SELECT year, Cause_Recode_39, MAX(ct_death),Age_Value
                        FROM (
                            SELECT year, Cause_Recode_39, Age_Value, Count(Cause_Recode_39) as ct_death
                            FROM mortality
                            GROUP BY year, Cause_Recode_39, Age_Value
                            )
                        GROUP BY Age_Value, year
                        ORDER BY Age_Value, ct_death desc""")

        data = [{"year":int(year),
                 "cause":int(cause),
                 "maxDeath": maxNum,
                 "age":Age} for (year, cause, maxNum, Age,) in  cur.fetchall()]
        conn.close()
        return {"data":data}

    except: 
        print "ERROR!!!"
        conn.close()
        raise
        
# get all data
    
@get('/text/<number>')
def textdata (number):
    if number =="one":
        return getAvgAgeFromCause()
    elif number =="two":
        return getMaxCauseForAge()
    else:
        return "no such numbers"
       
@get('/data')
def data ():
    return pullData()
    
@get('/<name>')
def static (name="project4.html"):
    return static_file(name, root='.')  # os.getcwd())


def main (p):
    run(host='0.0.0.0', port=p)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        print "Usage: server <port>"

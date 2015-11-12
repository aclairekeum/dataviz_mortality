#
# A simple server for mortality data
#
# Requires the bottle framework
# (sufficient to have bottle.py in the same folder)
#
# run with:
#
#    python mortality-server-2.py 8080
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
        cur.execute("""SELECT year, Cause_Recode_39, sex, education, SUM(1) as total 
                       FROM mortality
                       GROUP BY year, Cause_Recode_39, sex, education""")
        data = [{"year":int(year),
                 "cause":int(cause),
                 "gender":sex,
                 "education":education,
                 "total":total} for (year, cause, sex, education, total,) in  cur.fetchall()]
        conn.close()

        causes = list(set([int(r["cause"]) for r in data]))
        genders = list(set([r["gender"] for r in data]))
        education = list(set([r["education"] for r in data]))
        return {"data":data, 
                "genders":genders,
                "causes":causes,
                "education":education}

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

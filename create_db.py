

import sqlite3

def create_db():
    con=sqlite3.connect(database="rms.db")
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS course(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text,duration text,charges text,description text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS student(roll text ,name text,email text,gender text,dob text,contact text,admission text,course text,state text,city text,pin text,address text,  PRIMARY KEY (roll, course))")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS result(roll text,name text,course text,marks_ob text,full_marks text,per text, PRIMARY KEY (roll, course) )")
    con.commit()
    con.close()


if __name__=="__main__":
    create_db()
    print("Database created successfully")
    
    




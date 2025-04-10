

import sqlite3

def create_db():
    con=sqlite3.connect(database="rms.db")
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS course(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text,duration text,charges text,description text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS student(roll text PRIMARY KEY ,name text,email text,gender text,dob text,contact text,admission text,course text,state text,city text,pin text,address text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS result(rid INTEGER PRIMARY KEY AUTOINCREMENT,roll text,name text,course text,marks_ob text,full_marks text,per text)")
    con.commit()
    con.close()


if __name__=="__main__":
    create_db()
    print("Database created successfully")
    con = sqlite3.connect("rms.db")
    cur = con.cursor()
    cur.execute("INSERT INTO course (name, duration, charges, description) VALUES ('Python', '3 months', '20000', 'Python programming language')")
    con.commit()
    cur.execute("INSERT INTO student(roll, name, email, gender, dob, contact, admission, course, state, city, pin, address) VALUES ('1001', 'John Doe', 'john.doe@example.com', 'Male', '1995-05-15', '1234567890', '2023-01-10', 'Python', 'California', 'Los Angeles', '90001', '123 Main St')")
    cur.execute("INSERT INTO result(roll, name, course, marks_ob, full_marks, per) VALUES ('1', 'John Doe', 'Python', '85', '100', '85')")
    con.commit()
    




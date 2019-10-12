# Team "camelCase"
# Matthew Chan & Jionghao Wu
# SoftDev1 pd2
# K#18: Average
# 2019-10-12

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O
import math      #facilitate averaging of grades


DB_FILE="../17_csv2db/discobandit.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

#==========================================================
# Facilitates adding rows to the 'courses' table
# IMPORTANT NOTE: sqlite3 executions CANNOT be run through a function

def addCourse(code, mark, studentId):
    return ("INSERT INTO courses VALUES('%s', %d, %d);" % (code, mark, studentId))


# Testing adding rows to 'courses'
c.execute(addCourse("testclass", 100, 9))  # expected new avg = 77.5
c.execute(addCourse("testclass", 0, 6))    # expected new avg = 69.75

#==========================================================
# Tests printing 'SELECT'ed data
'''
q = "SELECT name, students.id, mark FROM courses, students WHERE courses.id = students.id;"

foo = c.execute(q)
print(foo) # prints a cursor object

for bar in foo: # prints each entry as a tuple
    print(bar)
'''
#==========================================================
# Collects and organizes data from the database created by '../17_csv2db/db_builder.py' into 'stu_avg' table
# IMPORTANT NOTE: sqlite3 executions will *OVERWRITE* one another in order; cannot store execution for later

studentDict = dict()
gradesDict = dict()

selectStudents = "SELECT name, id FROM students;"
studentData = c.execute(selectStudents)

for name, studentId in studentData:
    studentDict[studentId] = name
    gradesDict[studentId] = list()

selectGrades = "SELECT students.id, mark FROM courses, students WHERE courses.id = students.id;"
gradesData = c.execute(selectGrades)

for studentId, grade in gradesData:
    gradesDict[studentId].append(grade)

# helper function to average grades
def average(list):
    return (math.fsum(list)/len(list))

c.execute("CREATE TABLE stu_avg(name TEXT, id INTEGER, average REAL);")
for studentId, gradesList in gradesDict.items():
    c.execute("INSERT INTO stu_avg VALUES('%s', %d, %f);" % (studentDict[studentId], studentId, average(gradesList)))

#==========================================================


db.commit() #save changes
db.close()  #close database
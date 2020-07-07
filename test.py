from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
import json 
from bson import json_util
import jinja2
from datetime import date
import datetime

actualdate = datetime.datetime.now()
today=actualdate.strftime("%d-%m-%Y")
today=actualdate.strptime(today,"%d-%m-%Y")

app=Flask("__name__")
connection=MongoClient("mongodb+srv://admin:admin@cluster0.uvdng.mongodb.net/examly?retryWrites=true&w=majority")
db=connection.examly
user_collection1=db.user_master
user_collection2=db.notification_master
@app.route('/')
def index_show():
     return render_template('login.html')
     
@app.route('/profile', methods = ['POST','GET'])
def login():
   username = request.form['rid']
   password = request.form['pass']
   
   if(user_collection1.find({'user_id': username,'password':password}).count()>0):
      detail=user_collection1.find_one({'user_id':username})
      detail2=user_collection2.find({'user_id':username})
      old=[];new=[]
      for msg in detail2:
         expecteddate=msg['create_date']
         expecteddate = datetime.datetime.strptime(expecteddate,"%d-%m-%Y")
         if today > expecteddate:
            old.append(msg)
         else:
            new.append(msg)
      print(old,new)
      return render_template('profile.html',detail=detail,old=old,new=new)
   else:
      return "Invalid credentials"
   #l=list(collection.find({}))
   #return json.dumps(l, default=json_util.default)

if __name__ == '__main__':
   app.run(debug = True)
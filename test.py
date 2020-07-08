from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
import json 
from bson import json_util
import jinja2
from datetime import date 
import datetime
import uuid

actualdate = datetime.datetime.now()
today=actualdate.strftime("%d-%m-%Y")
today=actualdate.strptime(today,"%d-%m-%Y")
time = actualdate.strftime("%H-%M-%S")

app=Flask("__name__")
connection=MongoClient("mongodb+srv://admin:admin@cluster0.uvdng.mongodb.net/examly?retryWrites=true&w=majority")
db=connection.examly
user_collection1=db.user_master
user_collection2=db.notification_master
user_collection3=db.user_course_relation
@app.route('/')
def index_show():
   return render_template('login.html')

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
   jsdata = request.form['javascript_data']
   
   return jsdata

@app.route('/apicall1',methods=['GET','POST'])
def call1():
   if(request.method == 'POST'):
      some_json = request.get_json()
      course_name=some_json['course_name']
      for student_id in some_json['student_id_list']:
         user_collection3.update({'user_id':student_id,'course_name':course_name},{'user_id':student_id,'course_name':course_name},upsert=True)
         message_id=uuid.uuid1()
         user_collection2.insert_one({'user_id':student_id,'message_id':message_id,'message':course_name+' course is available','status':'unread','create_time':time,'create_date':today})
      return "updated successfully"

   else:
      return jsonify({'get call': "api call check"})

@app.route('/apicall2',methods=['GET','POST'])
def call2():
   if(request.method=='POST'):
      some_json = request.get_json()
      class_name=some_json['class_name']
      message_list=some_json['message_list']
      students_given_class=list(user_collection1.find({'class_name':class_name},{'user_id':1}))
      for student_given_class in students_given_class:
         student_given_class_id = student_given_class['user_id']
         for msg in message_list:
            message_id=uuid.uuid1()
            user_collection2.insert_one({'user_id':student_given_class_id,'message_id':message_id,'message':msg,'status':'unread','create_time':time,'create_date':today})
      return "updated successfully"

@app.route('/apicall3',methods=['GET','POST'])
def call3():
   if(request.method=='POST'):
      some_json = request.get_json()
      user_id=some_json['user_id']
      user_name=user_collection1.find_one({'user_id':user_id},{'name':1}) 
      friend_id_list=some_json['friend_id_list']
      course_name=some_json['course_name']
      for friend_id in friend_id_list:
         message_id=uuid.uuid1()
         user_collection2.insert_one({'user_id':friend_id,'message_id':message_id,'message':'Your friend '+user_name['name']+' has completed the '+course_name+' course','status':'unread','create_time':time,'create_date':today})

      return "updated successfully"

@app.route('/profile', methods = ['POST','GET'])
def login():
   username = request.form['rid']
   password = request.form['pass']
   
   if(user_collection1.find({'user_id': username,'password':password}).count()>0):
      detail=user_collection1.find_one({'user_id':username})
      detail2=user_collection2.find({'user_id':username})
      unread_count=user_collection2.find({'user_id':username,'status':'unread'}).count()
      old=[];new=[]
      for msg in detail2:
         expecteddate=msg['create_date']
         if today > expecteddate:
            old.append(msg)
            old=old[::-1]
         else:
            new.append(msg)
            new=new[::-1]
      return render_template('profile.html',detail=detail,old=old,new=new,unread_count=unread_count)
   else:
      return "Invalid credentials"
   #l=list(collection.find({}))
   #return json.dumps(l, default=json_util.default)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == '__main__':
   app.run(debug = True)
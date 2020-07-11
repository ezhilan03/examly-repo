from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_pymongo import PyMongo
from pymongo import MongoClient
import json 
from bson import json_util
import jinja2
from datetime import date 
import datetime
import uuid
import random
from timeit import default_timer as timer



actualdate = datetime.datetime.now()
today=actualdate.strftime("%d-%m-%Y")
today=actualdate.strptime(today,"%d-%m-%Y")
time = actualdate.strftime("%H-%M-%S")

app=Flask("__name__")
#key=uuid.uuid4().hex
#app.secret_key = key
connection=MongoClient("mongodb+srv://admin:admin@cluster0.uvdng.mongodb.net/examly?retryWrites=true&w=majority")
db=connection.examly
user_collection1=db.user_master
user_collection2=db.notification_master
user_collection3=db.user_course_relation

@app.route('/')
def index_show():
   return render_template('login.html')

@app.route('/unread_to_read', methods = ['POST'])
def get_post_javascript_data():
   if(request.method == 'POST'):
      jsdata = request.form['javascript_data']
      user_collection2.update_many({'user_id':username,'status':'unread'},{"$set":{'status':'read'}})
      return jsdata

@app.route('/to_clicked', methods = ['POST'])
def get_post_javascript_data2():
   if(request.method == 'POST'):
      jsdata = request.form['javascript_data']
      user_collection2.update({'message_id':jsdata},{"$set":{'status':'clicked'}})
      return jsdata

@app.route('/apicall1',methods=['GET','POST'])
def call1():
   if(request.method == 'POST'):

      some_json = request.get_json()
      course_name=some_json['course_name']
      apicall1_list=[]
      print(some_json['student_id_list'])
      for student_id in some_json['student_id_list']:
         message_id=str(uuid.uuid1())
         apicall1_list.append({'user_id':student_id,'message_id':message_id,'message':course_name+' course is available','status':'unread','create_time':time,'create_date':today})
      user_collection2.insert_many(apicall1_list)
      return "updated successfully"

   else:
      return jsonify({'get call': "api call check"})

@app.route('/apicall2',methods=['GET','POST'])
def call2():
   if(request.method=='POST'):
      start=timer()

      some_json = request.get_json()
      class_name1=some_json['class_name']
      class_name=class_name1.upper()
      message_list=some_json['message_list']
      staff_name=some_json['staff_name']
      
      students_given_class=list(user_collection1.find({'class_name':class_name},{'user_id':1}))
      count2=0
      for msg in message_list:
         apicall2_list=[]
         for student_given_class in students_given_class:
            student_given_class_id = student_given_class['user_id']
            message_id=str(uuid.uuid1())
            apicall2_list.append({'user_id':student_given_class_id,'message_id':message_id,'message':staff_name+' : '+msg,'status':'unread','create_time':time,'create_date':today})   
         user_collection2.insert_many(apicall2_list)
         count2+=len(apicall2_list)
      end=timer()
      a="updated successfully.\n No of notifications:"+str(count2)+"\nTime taken :"+str(end-start)+" seconds"
      return a

@app.route('/apicall3',methods=['GET','POST'])
def call3():
   if(request.method=='POST'):
      some_json = request.get_json()
      user_id=some_json['user_id']
      user_name=user_collection1.find_one({'user_id':user_id},{'name':1}) 
      friend_id_list=some_json['friend_id_list']
      course_name1=some_json['course_name']
      apicall3_list=[]
      course_name=course_name1.capitalize()
      for friend_id in friend_id_list:
         message_id=str(uuid.uuid1())
         apicall3_list.append({'user_id':friend_id,'message_id':message_id,'message':'Your friend '+user_name['name']+' has completed the '+course_name+' course','status':'unread','create_time':time,'create_date':today})
      user_collection2.insert_many(apicall3_list)

      return "updated successfully"

@app.route('/apicall4',methods=['GET','POST'])
def call4():
   if(request.method=='POST'):
      some_json = request.get_json()
      course_name1=some_json['course_name']
      course_name=course_name1.capitalize()
      apicall4_list=[]
      remainder_id_list=list(user_collection3.find({'course_name':course_name}))
      for remainder_id in remainder_id_list:
         message_id=str(uuid.uuid1())
         apicall4_list.append({'user_id':remainder_id['user_id'],'message_id':message_id,'message':'The '+course_name+' course you enrolled is about to start','status':'unread','create_time':time,'create_date':today})
      user_collection2.insert_many(apicall4_list)
      return "updated successfully"
@app.route('/profile', methods = ['POST','GET'])
def login():
   
   if(user_collection1.find({'user_id': username,'password':password}).count()>0):
      detail=user_collection1.find_one({'user_id':username})
      detail2=user_collection2.find({'user_id':username})
      unread_count=user_collection2.find({'user_id':username,'status':'unread'}).count()
      old=[];new=[]
      for msg in detail2:
         expecteddate=msg['create_date']
         if today > expecteddate:
            old.append(msg)
         else:
            new.append(msg)
      new=new[::-1]
      old=old[::-1]    
      return render_template('profile.html',detail=detail,old=old,new=new,unread_count=unread_count)
   else:
      return "Invalid credentials"

@app.route('/logout')
def logout():
   
   return redirect('/')

@app.route('/login2', methods = ['POST','GET'])
def login2():
   global username
   global password
   username = request.form['rid']
   password = request.form['pass']
   
   return redirect('/profile')

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == '__main__':
   app.run(debug = True)
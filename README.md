Examly-app
=====
This is a complete in-app notification system  for a sample classroom website built using the Flask framework.

* * *
I have imported the following modules:
* Flask 
* PyMongo to access the mongodb database
* jinja2 to write python codes in html file 
* datetime to label the date of notification creation along with the notification
* uuid and random to generate random message_id
* default_timer to find the run time of second apicall which sends multiple messages to multiple users. 

# Code
- First it calculates the date and time and store it in variables
- Then a Flask object is created.
- Connection is made to the Mongodb server and the collections in the database in given to variables.
- Code contains a total of 9 functions.
## Functions
### index_show():
It is routed to the home page and it renders the login.html file
### get_post_javascript_data():
This function is called when any "read but not clicked" notification is clicked. The profile.js file returns the message_id so this function updates the notification's status to "clicked".
### call1:
This function is for the api call to trigger Notification type 1. It gets the course_name and student_id_list and loops through the list to crate notification document with message_id generated randomly each time. Instead of inserting one document at a time we append all the documents in an empty list and did insert_many.
### call2:
This function is for the api call to trigger Notification type 2.It gets the class_name, message_list and staff_name and find the list of students who belongs to the given class_name. First a for loop for the message_list and for each message an empty list is created and then a loop for the students list within which we generate notifocation document with unique message_id is appended into apicall2_list. And the end of the first loop the list of documents is inserted into database which is quite optimal solution without doing a large number of inserts and not getting Memory error. The number of notifications is calculated and the running time is calculated from subtracting end time and start time are returned.
### call3:
This function is for the api call to trigger Notification type 3. It gets the user_id, friend_id_list and course_name and finds the name of the user using user_id. Loops through the list of friend ids and append a message with unique message_id to an empty list. the list of documents is inserted using insert_many.
### call4:
This function is for the api call to trigger Notification type 4. It gets the course_name and finds the list of ids of students who are registered for the given course. Loops through the list and append the notification document to an empty list. The list of notifications is inserted using insert_many.
### login:
When the submit button in login.html is clicked, this function is called. It stores the user-id and password from the form and only if the password is valid it will proceed otherwise it returns a "Invalid credentials" string. It finds the number of unread messages for the user, user_master data and notification master data for the user. It loops through the messages and append message to old list if the date of the message created is less than (i.e before) the date of the program being executed. Reversing the both list so that it will be in the order of latest to old messages. It renders the profile.html by passing some values to display it.
### logout:
This function is called when logout button in profile.html is clicked. It redirects to the home page.

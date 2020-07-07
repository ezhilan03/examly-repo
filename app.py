from flask import Flask, render_template
from flask_pymongo import PyMongo

app=Flask("__name__")
app.config["MONGO_URI"] = "mongodb://localhost:27017/testdb"
mongo = PyMongo(app)

@app.route("/")
def index():
    users=mongo.db.user_credentials.find()
    return render_template('login.html',users=users)

if __name__=="__main__":
    app.run(debug=True)
import os
from datetime import datetime
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

def write_to_file(filename, data):
    with open(filename, "a") as file:
        file.writelines(data)

def add_messages(username, message):
    
    write_to_file("data/messages.txt", "({0}) {1} - {2}\n".format(
            datetime.now().strftime("%H:%M:%S"),
            username.title(), 
            message))
    
    
def get_all_messages():
    messages = []
    with open("data/messages.txt", "r") as chat_messages:
        messages = chat_messages.readlines()
    return messages    

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        write_to_file("data/users.txt", request.form["username"] + "\n")
        return redirect(request.form["username"])    
    return render_template("index.html")
    
    
@app.route('/<username>')
def user(username):
    messages = get_all_messages()
    return render_template("chat.html", 
                              username=username, chat_messages=messages)
    
@app.route('/<username>/<message>') 
def send_message (username, message):
    add_messages(username, message)
    return redirect(username)

    
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
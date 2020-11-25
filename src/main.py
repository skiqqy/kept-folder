# Needed libs
from flask import Flask, render_template, request
from hashlib import sha256
from datetime import datetime
from os import system

# My libs
import helper

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route("/genkey", methods = ["GET"])
def genkey():
    nic = request.args.get('nic').lower()

    if helper.search_key(nic) == None: # Check that this user does not have a key
        val = sha256((nic + str(datetime.now())).encode('utf-8')).hexdigest()
        helper.write_keyval(nic, val, misc=str(datetime.now())) # Generate and store the key
        system("mkdir disk/users/" + nic)
        return render_template('key_success.html', nic=nic, key=val)
    else:
        error = str("Failed to generate a key for '%s', a key already exists." % nic)
        return render_template('error.html', etype='key', error=error)

def setup():
    app.template_folder = "../assets/templates/"

setup()

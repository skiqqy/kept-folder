# Needed libs
from flask import Flask, render_template, request, jsonify
from hashlib import sha256
from datetime import datetime
from os import system
from helper import append_log as log
from helper import ret_status as ret_status

# My libs
import helper

work_dir = 'disk'
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
        template = render_template('key_success.html', nic=nic, key=val)
        status="SUCCESS"
    else:
        error = str("Failed to generate a key for '%s', a key already exists." % nic)
        template = render_template('error.html', etype='key', error=error)
        status="FAILED"

    log("genkey attempt [%s] -> nic:%s, ip:%s" % (status, nic, request.remote_addr))
    return template

@app.route("/take/note", methods = ["POST"])
def takenote():
    try:
        nic = request.form.get('nic').lower()
        key = request.form.get('key').lower()
        fname = request.form.get('fname').lower()
        content = request.form.get('content').lower()
    except:
        return ret_status(1, route=str("/take/note from %s" % request.remote_addr))

    log_key = helper.search_key(nic)
    if log_key!= None:
        if log_key.split('^')[1] == key:
            code = 0
            f = open(str('%s/users/%s/%s' % (work_dir, nic, fname)), "w") # open the file
            f.write(content)
            f.close()
        else:
            code = 2
    else:
        code = 3
    return ret_status(code, route=str("/take/note from %s" % request.remote_addr))

def setup():
    app.template_folder = "../assets/templates/"

setup()

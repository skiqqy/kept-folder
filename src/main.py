# Needed libs
from flask import Flask, render_template, request, jsonify
from hashlib import sha256
from datetime import datetime
from os import system
from os import getenv
from helper import append_log as log
from helper import ret_status as ret_status

# My libs
import helper

work_dir = 'disk'
KEPT_FOLDER_AC = False
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route("/genkey", methods = ["GET"])
def genkey():
    if not KEPT_FOLDER_AC:
        error = "Account creation is currently disabled."
        return render_template('error.html', etype='Account Creation', error=error)
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

@app.route("/upload/note", methods = ["POST"])
def takenote():
    try:
        nic = request.form.get('nic').lower()
        key = request.form.get('key').lower()
        fname = request.form.get('fname').lower()
        content = request.form.get('content').lower()
    except:
        return ret_status(1, route=str("/upload/note from %s" % request.remote_addr))

    log_key = helper.search_key(nic)
    if log_key!= None:
        if log_key.split('^')[1] == key:
            code = 0
            f = open('%s/users/%s/%s' % (work_dir, nic, fname), "w") # open the file
            f.write(content + '\n')
            f.close()
            log('[FILE IO] ./%s/users/%s/%s from %s' % (work_dir, nic, fname, request.remote_addr))
        else:
            code = 2
    else:
        code = 3
    return ret_status(code, route=str("/upload/note from %s" % request.remote_addr))

@app.route("/download/note", methods = ["POST"])
def givenote():
    data = None
    try:
        nic = request.form.get('nic').lower()
        key = request.form.get('key').lower()
        fname = request.form.get('fname').lower()
    except:
        return ret_status(1, route=str("/download/note from %s" % request.remote_addr))

    log_key = helper.search_key(nic)
    if log_key!= None:
        if log_key.split('^')[1] == key:
            try:
                f = open('%s/users/%s/%s' % (work_dir, nic, fname), "r").read().splitlines() # Open for reading
                content = ''
                for s in f:
                    content += s + '\n'
                data = {'content':content, 'fname':fname}

                log('Sending ./%s/users/%s/%s to %s' % (work_dir, nic, fname, request.remote_addr))
                code = 0
            except:
                code = 4
        else:
            code = 2
    else:
        code = 3
    return ret_status(code, data=data, route=str("/download/note from %s" % request.remote_addr))

def setup():
    global KEPT_FOLDER_AC
    if getenv("KEPT_FOLDER_AC") == "1":
        KEPT_FOLDER_AC = True
    app.template_folder = "../assets/templates/"

setup()

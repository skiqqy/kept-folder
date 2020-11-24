from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route("/genkey", methods = ["GET"])
def genkey():
    nic = request.args.get('nic')
    key = "TODO"

    # TODO: Check that this user does not have a key
    if True:
        # TODO: Store this users key.
        return render_template('key_success.html', nic=nic, key=key)
    else:
        error = str("Failed to generate a key for '%s', a key already exists." % nic)
        return render_template('error.html', etype='key', error=error)

def setup():
    app.template_folder = "../assets/templates/"

setup()

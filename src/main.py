from flask import Flask, render_template
import sys
print(sys.__name__)

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

def setup():
    app.template_folder = "../assets/templates/"

setup()

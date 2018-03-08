from flask import Flask, render_template, request, session, send_file
import os
import sqlite3 as sql
import time
import datetime
import pdb
app = Flask(__name__)
lid = 990
global msg



@app.route('/')
def home():
      return render_template('home.html')


app.secret_key = os.urandom(12)

if __name__ == '__main__':
    app.run(debug = True, threaded=True)
from flask import Flask, render_template, request, redirect, send_file
from pymysql import connections
import os
import random
import argparse
import boto3
import botocore
import io


app = Flask(__name__)

DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "passwors"
DATABASE = os.environ.get("DATABASE") or "employees"
BACKGROUND_FROM_ENV = os.environ.get('APP_BACKGROUND') or "back1"
DBPORT = int(os.environ.get("DBPORT"))
S3_BUCKET = os.environ.get("S3_BUCKET")
S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")
S3_TOKEN = os.environ.get("S3_TOKEN")
GName = os.environ.get("GROUP_NAME")
AWS_REGION = os.environ.get("AWS_REGION")

print(" printing environment fetched dbhost name  --- " + str(DBHOST))  #for debugging purpose
print(" printing environment fetched group name  --- " + str(GName))  #for debugging purpose
print(" printing environment fetched s3 bucket name  --- " + str(S3_BUCKET))  #for debugging purpose

# Permission to S3 Bucket
app.config['S3_BUCKET'] = S3_BUCKET
app.config['S3_KEY'] = S3_KEY
app.config['S3_SECRET'] = S3_SECRET
app.config['S3_TOKEN'] = S3_TOKEN
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

s3 = boto3.resource("s3",
            aws_access_key_id=app.config['S3_KEY'],
            aws_secret_access_key=app.config['S3_SECRET'],
            aws_session_token=app.config['S3_TOKEN'],
            region_name=AWS_REGION
            )
            
#bucket = s3.Bucket(S3_BUCKET)
    
# Create a connection to the MySQL database
db_conn = connections.Connection(
    host= DBHOST,
    port=DBPORT,
    user= DBUSER,
    password= DBPWD, 
    db= DATABASE
    
)
output = {}
table = 'employee';

# Define the supported background
background_url = {
    "back1": "https://clo835-finals-group11.s3.amazonaws.com/back1.jpeg",
    "back2": "https://clo835-finals-group11.s3.amazonaws.com/back2.jpeg",
    "back3": "https://clo835-finals-group11.s3.amazonaws.com/back3.jpeg"
    }

# Create a string of supported backgrounds
SUPPORTED_BACKGROUND = ",".join(background_url.keys())

# Generate a random backgrounds
BACKGROUND = random.choice(["back1", "back2", "back3"])


@app.route("/", methods=['GET', 'POST'])
def home():
 
    return render_template('addemp.html', GROUP_NAME=GName, background=background_url[BACKGROUND])

@app.route("/about", methods=['GET','POST'])
def about():
    
    # Permission to S3 Bucket
    #s3 = boto3.resource("s3",
           # aws_access_key_id=S3_KEY,
           # aws_secret_access_key=S3_SECRET,
           # aws_session_token=S3_TOKEN,
           # region_name=AWS_REGION
           # )
    
    #s3.download_file(
    #bucket=(S3_BUCKET), Key="back1.jpeg", Filename="back1_local.jpeg"
    #)
    
    #s3.download_file(
    #bucket=(S3_BUCKET), Key="back2.jpeg", Filename="back2_local.jpeg"
    #)
    
    #s3.download_file(
    #bucket=(S3_BUCKET), Key="back3.jpeg", Filename="back3_local.jpeg"
    #)
        
    return render_template('about.html', GROUP_NAME=GName , background=background_url[BACKGROUND])
    
@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

  
    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        
        cursor.execute(insert_sql,(emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('addempoutput.html', name=emp_name, GROUP_NAME=GName, background=background_url[BACKGROUND])

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", GROUP_NAME=GName, background=background_url[BACKGROUND])


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql,(emp_id))
        result = cursor.fetchone()
        
        # Add No Employee found form
        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
        
    except Exception as e:
        print(e)

    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"], GROUP_NAME=GName, background=background_url[BACKGROUND])

if __name__ == '__main__':
    
    # Check for Command Line Parameters for background
    parser = argparse.ArgumentParser()
    parser.add_argument('--background', required=False)
    args = parser.parse_args()

    if args.background:
        print("Background from command line argument =" + args.background)
        BACKGROUND = args.background
        if BACKGROUND_FROM_ENV:
            print("A background was set through environment variable -" + BACKGROUND_FROM_ENV + ". However, background from command line argument takes precendence.")
    elif BACKGROUND_FROM_ENV:
        print("No Command line argument. Background from environment variable =" + BACKGROUND_FROM_ENV)
        BACKGROUND = BACKGROUND_FROM_ENV
    else:
        print("No command line argument or environment variable. Picking a Random BACKGROUND =" + BACKGROUND)

    # Check if input background is a supported one
    if BACKGROUND not in background_url:
        print("Background not supported. Received '" + BACKGROUND + "' expected one of " + SUPPORTED_BACKGROUND)
        exit(1)

    app.run(host='0.0.0.0',port=81,debug=True)

import pymysql, json, configparser, os
from flask import Flask, request
from flask_cors import cross_origin
from flask_api import status

path = os.path.abspath('.')
cfgpath = path.split('Capstone')[0] + 'Capstone/config.ini'

config = configparser.ConfigParser()
config.read(cfgpath)
print(cfgpath)
app = Flask(__name__)

@app.route('/store', methods = ['POST'])
@cross_origin()
def object_store():
    mysql = pymysql.connect(user = config['MYSQL']["user"], password = config['MYSQL']["password"], port = int(config["MYSQL"]["port"]), host = config['MYSQL']["host"])
    cur = mysql.cursor()
    data_json = {}
    
    Student_id = request.form.get('Student_id')
    
    check_account = cur.execute("SELECT * FROM Capstone.Information WHERE Student_id = '%s'"%(Student_id))
    print(check_account)
    if check_account == 0:
        Student_name = request.form.get('Student_name')
        Email = request.form.get('Email')
        Department = request.form.get('Department')
    
    INSERT = '''INSERT INTO Capstone.Information(
                                    Student_id,
                                    Student_name,
                                    Email,
                                    Department
                                    )VALUES(%s, %s, %s, %s);'''

    insert_data = (
        Student_id,
        Student_name,
        Email,
        Department
        )

    cur.execute(INSERT, insert_data)
    mysql.commit()

    data_json['Log'] = "Upload Success"

    return json.dumps(data_json), status.HTTP_200_OK

@app.route('/get', methods = ['GET'])
@cross_origin()
def object_information():
    mysql = pymysql.connect(user = config['MYSQL']["user"], password = config['MYSQL']["password"], port = int(config["MYSQL"]["port"]), host = config['MYSQL']["host"])
    cur = mysql.cursor()
    data_json = {}
    Student_id = request.args.get('Student_id')

    cur.execute('''SELECT * FROM Capstone.Information WHERE Student_id = '%s';''' %Student_id)
    data = cur.fetchall()
    if(len(data) == 0):
        data_json["Log"] = "Student ID is not exist!"
        return json.dumps(data_json), status.HTTP_400_BAD_REQUEST
    else: 
        
        data_json['Student_id'] = Student_id
        data_json['Student_name'] = data[0][1]
        data_json['Email'] = data[0][2]
        data_json['Department'] = data[0][3]

        return json.dumps(data_json), status.HTTP_200_OK



app.run(host = config['FLASK']['host'], port = int(config['FLASK']['port']), debug=True )

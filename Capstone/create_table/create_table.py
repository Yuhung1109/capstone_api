import pymysql, json, configparser, os, datetime

path = os.path.abspath('.')
cfgpath = path.split('Capstone')[0] + 'Capstone/config.ini'

config = configparser.ConfigParser()
config.read(cfgpath)


mysql = pymysql.connect(user = config['MYSQL']["user"], password = config['MYSQL']["password"], port = int(config["MYSQL"]["port"]), host = config['MYSQL']["host"])
cur = mysql.cursor()
cur.execute('''CREATE DATABASE IF NOT EXISTS Capstone;''')

cur.execute('''CREATE TABLE IF NOT EXISTS Capstone.Information (
                Student_id text NOT NULL,
                Student_name text NOT NULL,
                Email text NOT NULL,
                Department text NOT NULL
                );''')
mysql.commit()

cur.close()





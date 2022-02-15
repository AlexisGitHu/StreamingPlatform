import sys
import logging
import pymysql
import json

rds_host = "75.101.164.88"

username = "admin"
password ="password"
dbname = "youtube"

contadorLogin = 0

def lambda_handler(event , context):
    try:
        conn = pymysql.connect(rds_host, user=username, passwd=password, db=dbname, connect_timeout=10, port=3306)
    except pymysql.MySQLError as e:
        print (e)
        sys.exit()
        
    nombreUsuario=event["queryStringParameters"]["nombreUsuario"];
    fraseRecuperacion=event["queryStringParameters"]["fraseRecuperacion"];

    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT fraseRecuperacion, contrasena, iniciosIncorrectos FROM Users WHERE nombreUsuario='"+nombreUsuario+"';")
            fraseRecuperacionBBDD, contrasenaEnBBDD, iniciosIncorrectos = cur.fetchone()
            
            print(contrasenaEnBBDD)
            if(int(iniciosIncorrectos) < 3):
                if (fraseRecuperacion == fraseRecuperacionBBDD):
                    redirectPage = contrasenaEnBBDD
                else:
                    redirectPage = "incorrecto"
            else:
                    redirectPage = "blocked"
            
    except pymysql.MySQLError as e:    
        print (e)
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*' },
        'body' : json.dumps( { 'redirect': redirectPage} )
    }
#      

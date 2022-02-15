import json
import sys
import logging
import pymysql
import time
rds_host = "75.101.164.88"

username = "admin"
password ="password"
dbname = "youtube"


def lambda_handler(event, context):
    try:
        conn = pymysql.connect(rds_host, user=username, passwd=password, db=dbname, connect_timeout=10, port=3306)
    except pymysql.MySQLError as e:
        print (e)
        sys.exit()
        
    token = event["queryStringParameters"]["token"]
    
    listaRutaVideos = []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT nombreUsuario FROM Tokens WHERE token='"+token+"';")
            nombreUsuario = cur.fetchone()
            nombreUsuario = nombreUsuario[0].lower()
            
            nombreBucket = "http://distribuidosyoutube"+nombreUsuario+".s3.us-east-1.amazonaws.com/"
            
            
    except pymysql.MySQLError as e:    
        print (e)
    
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*' },
        'body':json.dumps({'user':nombreUsuario, 'bucket':nombreBucket})
    }


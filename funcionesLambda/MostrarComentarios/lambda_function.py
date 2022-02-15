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
    
    nombreVideo = event["queryStringParameters"]["nombreVideo"]
    urlVideo = event["queryStringParameters"]["urlVideo"]
    
    try:
        conn = pymysql.connect(rds_host, user=username, passwd=password, db=dbname, connect_timeout=10, port=3306)
    except pymysql.MySQLError as e:
        print (e)
        sys.exit()
        
    listaRutaVideos = []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT idVideo FROM Videos WHERE nombreVideo='"+nombreVideo+"' and rutaEnS3='"+urlVideo+"';")
            idVideo = cur.fetchone()
            print(idVideo)
            
            cur.execute("SELECT nombreUsuario, content, idComment FROM Comments WHERE idVideo='"+str(idVideo[0])+"' and idResp IS NULL;")
            comentarios = cur.fetchall()
            
            cur.execute("SELECT a.idResp, a.nombreUsuario, a.content, b.nombreUsuario AS alQueRespondemos, a.idComment from Comments a INNER JOIN Comments b ON b.idComment=a.idResp WHERE a.idVideo='"+str(idVideo[0])+"';")
            comentariosResp = cur.fetchall()
            
            
    except pymysql.MySQLError as e:    
        print (e)
    
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*' },
        'body':json.dumps({'comentarios':comentarios, 'comentariosResp':comentariosResp})
    }


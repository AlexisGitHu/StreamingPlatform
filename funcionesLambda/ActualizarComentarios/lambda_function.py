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
    
    token = event["queryStringParameters"]["token"]
    nombreVideo = event["queryStringParameters"]["nombreVideo"]
    urlVideo = event["queryStringParameters"]["urlVideo"]
    contenido = event["queryStringParameters"]["contenido"]
    
    try:
        alQueRespondemos = event["queryStringParameters"]["alQueRespondemos"]
        idComentario = event["queryStringParameters"]["idComentario"]
    except:
        alQueRespondemos = None
    
    print(token)
    print(nombreVideo)
    print(urlVideo)
    print(contenido)
    
    try:
        conn = pymysql.connect(rds_host, user=username, passwd=password, db=dbname, connect_timeout=10, port=3306)
    except pymysql.MySQLError as e:
        print (e)
        sys.exit()
        
    listaRutaVideos = []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT nombreUsuario FROM Tokens WHERE token='"+token+"';")
            nombreUsuario = cur.fetchone()
            nombreUsuario = nombreUsuario[0]
            
            cur.execute("SELECT idVideo FROM Videos WHERE nombreVideo='"+nombreVideo+"' and rutaEnS3='"+urlVideo+"';")
            idVideo = cur.fetchone()
            print(idVideo)
            if (alQueRespondemos == None):
                cur.execute("INSERT INTO Comments(nombreUsuario, idVideo, content) values ('"+nombreUsuario+"',"+str(idVideo[0])+",'"+contenido+"');")
                conn.commit()
            else:
                print(alQueRespondemos)
                print(idComentario)
                cur.execute("INSERT INTO Comments(nombreUsuario, idVideo, content, idResp) values ('"+nombreUsuario+"',"+str(idVideo[0])+",'"+contenido+"', "+str(idComentario)+");")
                conn.commit()
            
    except pymysql.MySQLError as e:    
        print (e)
    
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*' },
        'body':json.dumps({'ok':'ok'})
    }


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
            nombreUsuario = nombreUsuario[0]
            
            print(nombreUsuario)
            cur.execute("SELECT * FROM Videos WHERE nombreUsuario='"+nombreUsuario+"';")
            videos = cur.fetchall()
            
            votosP = {}
            votosN = {}
            
            for idVideo in videos:
                cur.execute("SELECT count(contentVote) as votosPos FROM VotesV WHERE idVideo="+str(idVideo[0])+" and contentVote=1;")
                numVideosPos = cur.fetchone()
                print("numVideosPos"+str(numVideosPos[0]))
                cur.execute("SELECT count(contentVote) as votosPos FROM VotesV WHERE idVideo="+str(idVideo[0])+" and contentVote=-1;")
                numVideosNeg = cur.fetchone()
                print("numVideosNeg"+str(numVideosNeg[0]))
                listaRutaVideos.append((idVideo[2], idVideo[5], numVideosPos[0], numVideosNeg[0]))
            
            
            
            # for video in videos:
            #     listaRutaVideos.append((video[2],video[5]))
            
            
    except pymysql.MySQLError as e:    
        print (e)
    
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*' },
        'body':json.dumps({'listavideos':listaRutaVideos})
    }


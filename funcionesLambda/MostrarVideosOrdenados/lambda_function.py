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
        
    listaRutaVideos = []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT idVideo, COUNT(contentVote) as votos FROM VotesV WHERE contentVote=1 GROUP BY idVideo ORDER BY votos DESC;")
            videos = cur.fetchall()
            
            print("videosConLikes:")
            print(videos)
            
            cur.execute("SELECT idVideo FROM Videos WHERE publico=true and idVideo NOT IN(SELECT idVideo FROM VotesV);")
            videosSinVotos = cur.fetchall()
            
            print("videosSinLikes:")
            print(videosSinVotos)
            
            for video in videos:
                print("videosConVotos")
                cur.execute("SELECT nombreVideo, rutaEnS3 FROM Videos WHERE idVideo="+str(video[0])+" and publico=true;")
                video_ordenado = cur.fetchone()
                print(video_ordenado)
                if(video_ordenado != None):
                    listaRutaVideos.append(video_ordenado)
            for video_sin in videosSinVotos:
                print("for videosSinVotos")
                cur.execute("SELECT nombreVideo, rutaEnS3 FROM Videos WHERE idVideo="+str(video_sin[0])+";")
                video_ordenado = cur.fetchone()
                print(video_ordenado)
                listaRutaVideos.append(video_ordenado)
                
    except pymysql.MySQLError as e:    
        print (e)
    
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*' },
        'body':json.dumps({'listavideos':listaRutaVideos})
    }


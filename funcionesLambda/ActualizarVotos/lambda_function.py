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
    voto = event["queryStringParameters"]["voto"]
    
    try:
        alQueRespondemos = event["queryStringParameters"]["alQueRespondemos"]
        idComentario = event["queryStringParameters"]["idComentario"]
    except:
        alQueRespondemos = None
    
    print("token="+token)
    print("nombreVideo="+nombreVideo)
    print("urlVideo="+urlVideo)
    print("voto="+voto)
    
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
            print("idVideo="+str(idVideo[0]))
            
            
            if (alQueRespondemos == None):
                cur.execute("SELECT contentVote FROM VotesV WHERE idVideo="+str(idVideo[0])+" and nombreUsuario='"+nombreUsuario+"';")
                votoAnteriorDelUsuario = cur.fetchone()
                if(votoAnteriorDelUsuario == None):
                    cur.execute("INSERT INTO VotesV(nombreUsuario, idVideo, contentVote) values ('"+nombreUsuario+"',"+str(idVideo[0])+","+voto+");")
                    conn.commit()
                elif(votoAnteriorDelUsuario[0] == int(voto)):
                    cur.execute("DELETE FROM VotesV WHERE nombreUsuario='"+nombreUsuario+"' and idVideo="+str(idVideo[0])+";")
                    conn.commit()
                else:
                    cur.execute("UPDATE VotesV SET contentVote="+voto+" WHERE nombreUsuario='"+nombreUsuario+"' and idVideo="+str(idVideo[0])+";")
                    conn.commit()
            else:
                print("alQueRespondemos="+alQueRespondemos)
                print("idComentario="+idComentario)
                cur.execute("SELECT contentVote FROM VotesC WHERE nombreUsuario='"+nombreUsuario+"' and idComment="+idComentario+";")
                votoAnteriorDelUsuario = cur.fetchone()
                if(votoAnteriorDelUsuario == None):
                    cur.execute("INSERT INTO VotesC(nombreUsuario, idComment, contentVote) values ('"+nombreUsuario+"',"+str(idComentario)+","+voto+");")
                    conn.commit()
                elif(votoAnteriorDelUsuario[0] == int(voto)):
                    cur.execute("DELETE FROM VotesC WHERE nombreUsuario='"+nombreUsuario+"' and idComment="+idComentario+";")
                    conn.commit()
                else:
                    cur.execute("UPDATE VotesC SET contentVote="+voto+" WHERE nombreUsuario='"+nombreUsuario+"' and idComment="+idComentario+";")
                    conn.commit()
            
    except pymysql.MySQLError as e:    
        print (e)
    
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*' },
        'body':json.dumps({'ok':'ok'})
    }


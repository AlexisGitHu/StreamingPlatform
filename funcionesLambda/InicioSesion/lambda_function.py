import sys
import logging
import pymysql
import json
import uuid

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
    contrasena=event["queryStringParameters"]["contrasena"];

    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT contrasena, iniciosIncorrectos FROM Users WHERE nombreUsuario='"+nombreUsuario+"';")
            contrasenaEnBBDD, iniciosIncorrectos = cur.fetchone()
            
            print (contrasena)
            print(contrasenaEnBBDD)
            if(int(iniciosIncorrectos) < 3):
                if (contrasenaEnBBDD == contrasena):
                    cur.execute("UPDATE Users SET iniciosIncorrectos=0 WHERE nombreUsuario='"+nombreUsuario+"';")
                    conn.commit()
                    
                    token = uuid.uuid4()
                    cur.execute("SELECT nombreUsuario FROM Tokens WHERE nombreUsuario='"+nombreUsuario+"';")
                    nombreUsuarioEnTokens = cur.fetchone()
                    
                    if(nombreUsuarioEnTokens != None):
                        cur.execute("DELETE FROM Tokens WHERE nombreUsuario='"+nombreUsuario+"';")
                        conn.commit()
                        
                    cur.execute("INSERT INTO Tokens(nombreUsuario, token) values ('"+nombreUsuario+"', '"+str(token)+"');")
                    conn.commit()
                    
                    redirectPage = "http://davidgdistribuidosutad.s3.amazonaws.com/paginaPrincipal.html"+"?token="+str(token)
                else:
                    cur.execute("UPDATE Users SET iniciosIncorrectos=iniciosIncorrectos+1 WHERE nombreUsuario='"+nombreUsuario+"';")
                    conn.commit()
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

import json
import sys
import logging
import pymysql
import time
import urllib.parse
import boto3
import math

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   tamano = str(s)+size_name[i]
   return tamano
   
print('Loading function')

s3 = boto3.client('s3')

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
        
    nombreUsuario=event["queryStringParameters"]["nombreUsuario"]
    nombreVideo=event["queryStringParameters"]["nombreVideo"]
    nombreFichero = event["queryStringParameters"]["nombreFichero"]
    etiquetaVideo=event["queryStringParameters"]["etiquetaVideo"]
    publico=event["queryStringParameters"]["publico"]
    
    bucket = "distribuidosyoutube"+nombreUsuario
    key = nombreFichero
    
    time.sleep(5)
    
    response = s3.get_object(Bucket=bucket, Key=key)
    
    tamano=response["ContentLength"]
    tamano = convert_size(tamano)
    rutaS3 = "https://distribuidosyoutube"+nombreUsuario+".s3.amazonaws.com/"+nombreFichero
    
    
    fecha = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        with conn.cursor() as cur:
            cur.execute("insert into Videos(nombreUsuario,nombreVideo,etiquetas,tamano,rutaEnS3,fechaSubida,publico) values ('" + nombreUsuario+"', '"+nombreVideo+"', '"+etiquetaVideo+"', '"+tamano+"', '"+rutaS3+"','"+fecha+"',"+publico+" );")
            conn.commit()
            
            
    except pymysql.MySQLError as e:    
        print (e)
    
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*' },
        'body':json.dumps({})
    }


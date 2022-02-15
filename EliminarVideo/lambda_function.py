import json
import sys
import logging
import pymysql
import time
import boto3
s3 = boto3.resource('s3')

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
    
    rutaVideo = event["queryStringParameters"]["rutaEnS3"]
    nombreVideo = event["queryStringParameters"]["nombreVideo"]
    
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Videos WHERE rutaEnS3='"+rutaVideo+"' and nombreVideo='"+nombreVideo+"';")
            terminaBucket = rutaVideo.index(".")
            bucket = rutaVideo[8:terminaBucket]
            
            empiezaNombre = rutaVideo.rfind("/")
            nombreVideoEnBucket = rutaVideo[empiezaNombre+1:]
            print(bucket)
            print(nombreVideoEnBucket)
            thumbnail = nombreVideoEnBucket+"_thumb.gif"
            s3.Object(bucket, nombreVideoEnBucket).delete()
            s3.Object(bucket, thumbnail).delete()
            conn.commit()
            
        
            
    except pymysql.MySQLError as e:    
        print (e)
    
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*' },
        'body':json.dumps({'ok':'ok'})
    }


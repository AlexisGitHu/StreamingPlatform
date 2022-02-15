import sys
import logging
import pymysql
import json


import logging
import boto3
s3 = boto3.client('s3')
s3_1 = boto3.resource('s3')

rds_host = "75.101.164.88"

username = "admin"
password ="password"
dbname = "youtube"



def lambda_handler(event , context):
    try:
        conn = pymysql.connect(rds_host, user=username, passwd=password, db=dbname, connect_timeout=10, port=3306)
    except pymysql.MySQLError as e:
        print (e)
        sys.exit()
        
    nombreCompleto=event["queryStringParameters"]["nombreCompleto"];
    nombreUsuario=event["queryStringParameters"]["nombreUsuario"];
    correoElectronico=event["queryStringParameters"]["correoElectronico"];
    contrasena=event["queryStringParameters"]["contrasena"];
    fraseRecuperacion=event["queryStringParameters"]["fraseRecuperacion"];
  

    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT nombreUsuario FROM Users WHERE nombreUsuario='"+nombreUsuario+"';")
            nombre = cur.fetchone()
            
            redirectPage = "http://davidgdistribuidosutad.s3-website-us-east-1.amazonaws.com/login.html"
            
            if nombre:
                redirectPage = "User no valido"
                
            else:
                nombreBucket = "distribuidosyoutube"+nombreUsuario.lower()
                s3.create_bucket(Bucket=nombreBucket)
                
                s3.put_bucket_notification_configuration(
                    Bucket = nombreBucket,
                    NotificationConfiguration={
                        'LambdaFunctionConfigurations': [
                        {
                            
                            'LambdaFunctionArn': 'arn:aws:lambda:us-east-1:787265103955:function:crearThumbnail',
                            'Events': [
                                's3:ObjectCreated:*'
                            ],
                            'Filter': {
                                'Key': {
                                    'FilterRules': [
                                        {
                                            'Name': 'suffix',
                                            'Value': '.mp4'
                                        },
                                    ]
                                }
                            }
                        },
                    ]})
                cur.execute("insert into Users values ('" + nombreCompleto+"', '"+nombreUsuario+"', '"+correoElectronico+"', '"+contrasena+"', '"+fraseRecuperacion+"',0);")
                conn.commit()
                
    except pymysql.MySQLError as e:    
        print (e)
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*' },
        'body' : json.dumps( {'redirect': redirectPage} )
    }
#      

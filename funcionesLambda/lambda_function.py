import json
import logging
import subprocess

import boto3
import uuid
import os

from urllib.parse import unquote_plus

def lambda_handler(event, context):
     #xml_output = subprocess.check_output(["./exodus/bin/ffmpeg",
     #                                   "-y" ,"-hide_banner" ,
     #                                   "-loglevel", "panic",
     #                                   "-i", "https://pruebacalculadora.s3.eu-west-2.amazonaws.com/gl.mkv",
     #                                   "-ss", "00:00:00", 
     #                                   "-vframes" , "1",
     #
     #                              "/tmp/out.png"])
    print(str(event))
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        path_file=os.path.split(key)
        
        thumb_filename=path_file[1]+"_thumb.gif"
        output_thumb="/tmp/"+thumb_filename
        xml_output=subprocess.check_output(["./exodus/bin/ffmpeg",
                                        "-y" ,"-hide_banner" ,
                                        "-loglevel", "panic",
                                        "-i", "https://"+bucket+".s3.us-east-1.amazonaws.com/"+key,
                                        "-ss", "00:00:00", 
                                        "-t" , "3",
                                        "-filter_complex","[0:v] fps=4,scale=240:-1",
                                        output_thumb])
        s3 = boto3.resource("s3")
        upload_gif=thumb_filename
        if(path_file[0]!=""):
            upload_gif=path_file[0]+"/"+thumb_filename
        s3.Bucket(bucket).upload_file(output_thumb,upload_gif,ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/gif'})
        # video = s3.Object(bucket, key)
        # video.copy_from(CopySource={'Bucket': bucket,'Key': key},MetadataDirective="REPLACE",ContentType="video/mp4", ACL='public-read')
        # msg="""
        #     <html>
        #     <header><title>Fichero subido</title></header>
        #     <body>
        #     Fichero subido <p/> <a href="http://""" + bucket+""".s3-website-us-east-1.amazonaws.com/player.html"> Ver video</url>
        #     </body>
        #     </html>""";
        # encoded_string = msg.encode("utf-8")
        # file_name = "success.html"
        # s3 = boto3.resource("s3")
        # s3.Bucket(bucket).put_object(Key=file_name, Body=encoded_string,ContentType='text/html')
        # object_acl = s3.ObjectAcl(bucket,file_name)
        # object_acl.put(ACL   = 'public-read')

        # msg="""<!DOCTYPE html>
        #     <html>
        #     <head>
        #     <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
        #     </head>
        #     <body >
        #     <video width="320" height="240" controls>
        #     <source src="https://"""+bucket+""".s3.amazonaws.com/"""+key+"""" type="video/mp4">
        #     Your browser does not support the video tag.
        #     </video>
        #     </body>
        #     </html>""";
        # file_name = "player.html"
        # encoded_string = msg.encode("utf-8")
        # s3.Bucket(bucket).put_object(Key=file_name, Body=encoded_string,ContentType='text/html')
        # object_acl = s3.ObjectAcl(bucket,file_name)
        # object_acl.put(ACL   = 'public-read')
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*' },
        'body':json.dumps({ 'output' :  'ok' })
    }



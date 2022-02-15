import json
import boto3


def lambda_handler(event, context):
    s3 = boto3.resource("s3")
    s3.Bucket(bucket).put_object(Key=file_name, Body=encoded_string,ContentType='text/html')
    object_acl = s3.ObjectAcl(bucket,file_name)
    object_acl.put(ACL   = 'public-read')

    msg="""<!DOCTYPE html>
        <html>
        <head>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
        </head>
        <body >
        <video width="320" height="240" controls>
        <source src="https://"""+bucket+""".s3.amazonaws.com/"""+key+"""" type="video/mp4">
        Your browser does not support the video tag.
        </video>
        </body>
        </html>""";
    file_name = "player.html"
    encoded_string = msg.encode("utf-8")
    s3.Bucket(bucket).put_object(Key=file_name, Body=encoded_string,ContentType='text/html')
    object_acl = s3.ObjectAcl(bucket,file_name)
    object_acl.put(ACL   = 'public-read')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

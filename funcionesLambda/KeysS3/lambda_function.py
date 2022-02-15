import json

import sys, os, base64, datetime, hashlib, hmac 

access_key = 'ASIA3OTFIFBJ5CPTGNPB'
secret_key = 'J3utJ01gGsFJH7uGS3muZMFIuKgYt7NprUjDQAiG'
securityToken= 'FwoGZXIvYXdzELj//////////wEaDBS5r+ayUEHxydLPciK8AR27pT2bPksK6GLe81iO1LCsFxGUVnBEZY2s55to9VNVERTF+YRFzDsDJRQG/DCG/bFGcDsbnShF5arTv2L2jH1Av1XZf8w3saWgE5lknaaa4lDRgBFzn/BHxFqQKmGh1qCaqr/mU84/V7/TrN4hxGSb8pOTLkJhUucpqJC+rkvaepDgjPGqRz3wxZ7XZMrP4bKnWx5I6609cZ3HKpyfrg5gCIQ9091++oBcz594UwJormzA9VYycJhlgpb5KKKElo8GMi2LfJV7QtTb2Uz8CAG9Z6rBtdkgeen/rH+o24OcR6OOXXg31kwjHSssoD95kUI='

bucket = "davidgdistribuidosutad"
bucketUrl = "http://davidgdistribuidosutad.s3-website-us-east-1.amazonaws.com/"
region = 'us-east-1'
service = 's3'

t = datetime.datetime.utcnow()
amzDate = t.strftime('%Y%m%dT%H%M%SZ')
dateStamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope
    
policy = """{"expiration": "2022-12-30T12:00:00.000Z",
"conditions": [
{"bucket": \"""" + bucket +"""\"},
["starts-with", "$key", ""],
{"acl": "public-read"},
{"success_action_redirect": \""""+ bucketUrl+"""success.html"},
    {"x-amz-credential": \""""+ access_key+"/"+dateStamp+"/"+region+"""/s3/aws4_request"},
    {"x-amz-algorithm": "AWS4-HMAC-SHA256"},
    {"x-amz-date": \""""+amzDate+"""\" },
    {"x-amz-security-token": \"""" + securityToken +"""\"  },
    ["starts-with", "$x-amz-meta-NombreVideo", ""],
    ["starts-with", "$x-amz-meta-EtiquetaVideo", ""]
  ]
}"""

def funcionDePolicy():
    global access_key
    global secret_key
    global securityToken
    global bucket
    global bucketUrl
    global region
    global service
    global t
    global amzDate
    global dateStamp
    global policy
    global nombreUsuario
    
    paginaRedireccion = "http://davidgdistribuidosutad.s3-website-us-east-1.amazonaws.com/subirvideo.html?token="+token
    
    policy = """{"expiration": "2022-12-30T12:00:00.000Z",
    "conditions": [
    {"bucket": \"""" + bucket +"""\"},
    ["starts-with", "$key", ""],
    {"acl": "public-read"},
    {"success_action_redirect": \""""+paginaRedireccion+"""\"},
        {"x-amz-credential": \""""+ access_key+"/"+dateStamp+"/"+region+"""/s3/aws4_request"},
        {"x-amz-algorithm": "AWS4-HMAC-SHA256"},
        {"x-amz-date": \""""+amzDate+"""\" },
        {"x-amz-security-token": \"""" + securityToken +"""\"  },
        ["starts-with", "$x-amz-meta-NombreVideo", ""],
        ["starts-with", "$x-amz-meta-EtiquetaVideo", ""]
      ]
    }"""

# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning


nuevoBucket = None
nombreUsuario = None
token = None

def lambda_handler(event, context):
    global bucket
    global bucketUrl
    global nombreUsuario
    global token
    
    nombreUsuario=event["queryStringParameters"]["nombreUsuario"]
    token=event["queryStringParameters"]["token"]
    bucket = "distribuidosyoutube"+nombreUsuario
    bucketUrl = "http://"+bucket+".s3-website-us-east-1.amazonaws.com/"
    
    funcionDePolicy()
    
    # TODO implement
    stringToSign= b""
    stringToSign=base64.b64encode(bytes((policy).encode("utf-8")))

    
    signing_key = getSignatureKey(secret_key, dateStamp, region, service)
    signature = hmac.new(signing_key, stringToSign, hashlib.sha256).hexdigest()
    
    #print(dateStamp)
    #print(signature)
    print(policy)
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*' },
        'body':json.dumps({ 'stringSigned' :  signature , 'stringToSign' : stringToSign.decode('utf-8') , 'xAmzCredential' : access_key+"/"+dateStamp+"/"+region+ "/s3/aws4_request" , 'dateStamp' : dateStamp , 'amzDate' : amzDate , 'securityToken' : securityToken })
    }


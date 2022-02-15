

<?php

        $aws_access_key_id='ASIA3OTFIFBJ5CPTGNPB';
	
	$aws_secret_access_key='J3utJ01gGsFJH7uGS3muZMFIuKgYt7NprUjDQAiG';
	
	$aws_session_token='FwoGZXIvYXdzELj//////////wEaDBS5r+ayUEHxydLPciK8AR27pT2bPksK6GLe81iO1LCsFxGUVnBEZY2s55to9VNVERTF+YRFzDsDJRQG/DCG/bFGcDsbnShF5arTv2L2jH1Av1XZf8w3saWgE5lknaaa4lDRgBFzn/BHxFqQKmGh1qCaqr/mU84/V7/TrN4hxGSb8pOTLkJhUucpqJC+rkvaepDgjPGqRz3wxZ7XZMrP4bKnWx5I6609cZ3HKpyfrg5gCIQ9091++oBcz594UwJormzA9VYycJhlgpb5KKKElo8GMi2LfJV7QtTb2Uz8CAG9Z6rBtdkgeen/rH+o24OcR6OOXXg31kwjHSssoD95kUI=';

        $lambda_func='mostrarTodosLosVideos';
        $payload='{"queryStringParameters": {';

        foreach ($_GET as $key => $value) {

                $payload .= '"' . $key . '":"' . $value .'",';

        }

        $payload=substr($payload, 0, -1);

        $payload.='}}';

        $cmd=' AWS_ACCESS_KEY_ID='. $aws_access_key_id .

        ' AWS_SECRET_ACCESS_KEY='. $aws_secret_access_key .

        ' AWS_SESSION_TOKEN='. $aws_session_token . ' aws lambda invoke --function-name --region us-east-1 '. $lambda_func . ' /tmp/resp.json 2>&1';
        
        exec( $cmd,$result,$result2);

        header('Access-Control-Allow-Origin: *');

        $result=file_get_contents("/tmp/resp.json");

        $json=json_decode($result,true);

        echo json_encode($json['body']);
?>





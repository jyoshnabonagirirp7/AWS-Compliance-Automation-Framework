import boto3
import json


def lambda_handler(event, context):
   print("DEBUG Event:", event)
   s3 = boto3.client('s3')
   config_client = boto3.client('config')


   # AWS Config always sends this as a JSON string
   invoking_event = json.loads(event['invokingEvent'])


   if 'configurationItem' not in invoking_event:
       print("No configurationItem found in invoking_event. Probably a test event.")
       return {"status": "ignored"}


   config_item = invoking_event['configurationItem']
   bucket_name = config_item['resourceName']
   compliance = 'NON_COMPLIANT'


   # Check for tag key=config, value=lambda
   try:
       response = s3.get_bucket_tagging(Bucket=bucket_name)
       tags = response.get('TagSet', [])
       for tag in tags:
           if tag['Key'] == 'config' and tag['Value'] == 'lambda':
               compliance = 'COMPLIANT'
   except Exception as e:
       print(f"No tags or error fetching tags for {bucket_name}: {e}")


   evaluation = {
       'ComplianceResourceType': config_item['resourceType'],
       'ComplianceResourceId': config_item['resourceId'],
       'ComplianceType': compliance,
       'Annotation': 'Bucket must have tag config=lambda',
       'OrderingTimestamp': config_item['configurationItemCaptureTime']
   }


   # Send evaluation result
   return config_client.put_evaluations(
       Evaluations=[evaluation],
       ResultToken=event['resultToken']
   )

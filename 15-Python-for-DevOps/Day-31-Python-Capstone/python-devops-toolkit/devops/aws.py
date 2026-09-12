import boto3

def get_ec2_instances(region):
    ec2 = boto3.client('ec2', region_name=region)
    res = ec2.describe_instances()
    instances = []
    for r in res.get('Reservations', []):
        for i in r.get('Instances', []):
            instances.append({'id': i['InstanceId'], 'state': i['State']['Name']})
    return instances

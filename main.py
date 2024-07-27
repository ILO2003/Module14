import boto3
import schedule

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')
"""
reservations = ec2_client.describe = ec2_client.describe_instances()
for reservation in reservations['Reservations']:
    instances = reservation['Instances']
    for instance in instances:
        print(f"Status of {instance['InstanceId']} is {instance['State']['Name']}")
   # this has many attributes, it is good for detailed info
   """

def inst_status():
    statuses = ec2_client.describe_instance_status()
    for status in statuses['InstanceStatuses']:
        ins_status = status['instanceStatus']['Status']
        sys_status = status['SystemStatus']['Status']
        print(f"Instance {status['InstanceId']} status is {ins_status} and system status is {sys_tatus}")


schedule.every(30).seconds.do(inst_status)

while True:
    schedule.run_pending()


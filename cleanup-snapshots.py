import boto3
from operator import itemgetter

ec2_client = boto3.client('ec2', region_name='eu-north-1')

volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'tag:env',
                'Values': ['prod']
            }
        ]
    )
for volume in volumes['Volumes']:
    snapshots = ec2_client.describe_snapshots(
        OwnerIds=['self'],
        Filters=[
            {
                'Name': 'volume-id',
                'Values': [volume['VolumeId']]
            }
        ]
    )

date_sorted = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)


for snap in date_sorted[2:]:
    # list of snapshots, skip first 2 and delete rest
    resp = ec2_client.delete_snapshot(
        SnapshotId=snap['SnapshotId']
    )
    print(resp)




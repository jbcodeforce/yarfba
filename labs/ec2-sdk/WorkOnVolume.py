import json, boto3


client = boto3.client('ec2')

volumes = client.describe_volumes()

for volume in volumes['Volumes']:
    for attachment in volume['Attachments']:
        print(attachment['InstanceId'])
        print(attachment['State'])
        print(attachment['VolumeId'])
    print(volume['State'])
    print(volume['Size'])
    print(volume['VolumeType'])
    print(volume['AvailabilityZone'])
    print(volume['Encrypted'])
    print(volume['Iops'])
    print(volume['SnapshotId'])
    print(volume['MultiAttachEnabled'])
    print(volume['Throughput'])


print(json.dumps(volumes, indent=4, sort_keys=True, default=str))
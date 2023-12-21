import boto3, json

ec2 = boto3.client('ec2')
response = ec2.describe_instances()
print(json.dumps(response, indent=4, sort_keys=True, default=str))


# Create the EBS volume
volume = ec2.create_volume(
    AvailabilityZone='us-west-2a',
    Size=10,  # in GB
    VolumeType='gp2',
    MultiAttachEnabled=True,
    Encrypted=False,
    DryRun=True,
    Iops=100, # IOPS provisioned for the volume, represents the rate at which the volume accumulates I/O credits for bursting
)

# Wait for the volume to become available
volume.wait_until_available()

# Get the volume ID
volume_id = volume['VolumeId']

# Launch EC2 instance with the attached volume
instances = ec2.run_instances(
    ImageId='ami-1234567890abcdef0', 
    MinCount=1,
    MaxCount=1,
    InstanceType='t3.micro',
    KeyName='mykey',
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {
                'VolumeId': volume_id, 
                'DeleteOnTermination': True
            }
        }
    ]
)

# Get the instance ID
instance_id = instances['Instances'][0]['InstanceId']

print("Instance", instance_id, "created with volume", volume_id)
import redis, os

AWS_REGION= os.environ.get("AWS_REGION",default="us-west-2")
EC2_NAME= os.environ.get("EC2_NAME","ec2-54-186-109-129")

r = redis.Redis(host=EC2_NAME + '.' + AWS_REGION + '.compute.amazonaws.com', port=6379, decode_responses=True)


r.set('foo', 'bar')

aFooContent=r.get('foo')
print(aFooContent)
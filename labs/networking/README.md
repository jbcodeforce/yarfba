# A sample based on Networking Immersion Day workshop

The goal of this lab is to demonstrate how to route traffic from a remote client to a cluster of EC2 with Redis server.

## Needs

* 2 or 3 Redis Servers, each running within its own EC2. Can run in same AZ, but in production it will be at least 3 AZs. To simplify in one VPC.
* Put EC2 in ASG
* Get NLB to route traffic to Redis Server on port 6379. NLBs are in public subnets.
* Should we modify NLB routing when adding EC2 ?
* What happens when Redis server fails? 

## Source 

* [NLB routing](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/network-load-balancer-getting-started.html)
* [Running efficient workload with ASG and EC2 spot instances](https://pages.awscloud.com/Running-Efficient-and-Resilient-Workloads-at-Scale-with-EC2-Auto-Scaling-and-EC2-Spot_2021_1025-CMP_OD.html)
* [Scaling NLB target groups by connections:](https://aws.amazon.com/blogs/networking-and-content-delivery/scaling-nlb-target-groups-by-connections/) a solution that automatically scales backend connections of a NLB target group based on a fixed number of network connections. 

## How to deploy the solution

It used AWS CloudFormation to create resources:

* 1 VPC
* 1 public subnet
* 1 EC2 with REDIS in the subnet.
* Security group so the EC2 instances allo TCP access on the listener port and health check requests


The user-data for redis looks like:

```sh
sudo yum -y install gcc make # install GCC compiler
cd /usr/local/src 
sudo wget http://download.redis.io/redis-stable.tar.gz
sudo tar xvzf redis-stable.tar.gz
sudo rm -f redis-stable.tar.gz
cd redis-stable
sudo yum groupinstall "Development Tools"
sudo make distclean
sudo make
sudo yum install -y tcl
sudo cp src/redis-server /usr/local/bin/
sudo cp src/redis-cli /usr/local/bin/
redis-server --protected-mode no
```
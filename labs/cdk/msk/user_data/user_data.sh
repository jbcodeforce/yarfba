#!/bin/bash
yum update -y
yum install -y java-11
wget https://archive.apache.org/dist/kafka/3.4.1/kafka_2.12-3.4.1.tgz
tar -xzf kafka_2.12-3.4.1.tgz 
cd kafka_2.12-3.4.1/libs
# download the Amazon MSK IAM JAR file under kafka_2.12-<>/libs
wget https://github.com/aws/aws-msk-iam-auth/releases/download/v1.1.7/aws-msk-iam-auth-1.1.7-all.jar
cd ..
echo "security.protocol=SASL_SSL" >> bin/client.properties
echo "sasl.mechanism=AWS_MSK_IAM" >> bin/client.properties
echo "sasl.jaas.config=software.amazon.msk.auth.iam.IAMLoginModule required;" >> bin/client.properties
echo "sasl.client.callback.handler.class=software.amazon.msk.auth.iam.IAMClientCallbackHandler" >> bin/client.properties
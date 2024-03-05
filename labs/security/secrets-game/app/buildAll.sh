#!/bin/bash
scriptDir=$(dirname $0)

IMAGE_NAME=jbcodeforce/aws-quarkus-secretsmanager-demo

if [[ $# -eq 1 ]]
then
  TAG=$1
else
  TAG=1.0.0
fi

./mvnw clean package -DskipTests
docker build -f src/main/docker/Dockerfile.jvm -t  ${IMAGE_NAME}:${TAG} .
docker push ${IMAGE_NAME}:${TAG}
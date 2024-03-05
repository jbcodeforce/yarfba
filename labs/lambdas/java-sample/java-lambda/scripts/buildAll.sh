#!/bin/bash
scriptDir=$(dirname $0)

IMAGE_NAME=jbcodeforce/java-lambda
TAG=latest
if [[ $# -eq 1 ]]
then
  REPO=$1
else
  REPO=
fi

mvn compile dependency:copy-dependencies -DincludeScope=runtime
docker build -f src/main/docker/Dockerfile -t  ${IMAGE_NAME}:${TAG} .
docker tag  ${IMAGE_NAME}:${TAG}   ${REPO}/${IMAGE_NAME}:${TAG}
docker push ${REPO}/${IMAGE_NAME}:${TAG}

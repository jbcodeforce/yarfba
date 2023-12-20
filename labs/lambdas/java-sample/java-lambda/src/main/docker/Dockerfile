FROM public.ecr.aws/lambda/java:11
#COPY target/java-lambda-1.0.0.jar ${LAMBDA_TASK_ROOT}
COPY target/classes ${LAMBDA_TASK_ROOT}
COPY target/dependency/* ${LAMBDA_TASK_ROOT}/lib/
CMD [ "jbcodeforce.HandlerWeatherData::handleRequest" ]
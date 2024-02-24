# [Elastic MapReduce - EMR](https://aws.amazon.com/emr)

This is the managed service for big data solution implementation using petabyte-scale datasets.  It is used for data processing, interactive analytics, and ML using open-source frameworks such as [Apache Spark](https://spark.apache.org/), [Apache Hive](https://hive.apache.org/), [Apache Flink](https://flink.apache.org/), or [Presto](https://prestodb.io/).

It offers four different ways to deploy applications:

* Serverless
* On EC2: closest deployment environment to a YARN-based Hadoop platform
* On EKS: when EKS is the deployment standard
* On Outposts

EMR supports virtually unlimited storage capacity through the EMRFS backed by Amazon S3, which can be shared across multiple EMR clusters or Amazon EMR Serverless. It also supports HDFS backed by EBS volumes and instance stores.

## Value propositions

* No cluster to operate (with the Serverless deployment)
* Avoid over or under-provisioning resources
* Supports Apache Iceberg to create tables and query, merge, and insert data  
* Auto determination of resources, compute and memory, needed to run analytics jobs
* Automatically scales workers up or down based on the workload and parallelism required at every stage of the job graph
* Track usage cost by applications
* Easy integration with AWS Redshift, Athena, S3 and data ingestion platform like Kinesis, MSK
* Integrate with AWS Service Catalog for managing EMR applications, and AWS Lake Formation for fine grained access control to the data.

## EMR EC2 cluster

[EMR is a cluster](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-overview.html) of EC2 instances which are nodes in Hadoop (HDFS). We can use Reserved Instances and Spot instances to reduce costs. There are three node types:

* **Master nodes**: coordinate cluster, and distribution of data and tasks among other nodes. 
* **Core nodes**: run tasks and store data in the Hadoop Distributed File System (HDFS) 
* **Task nodes**: (optional)  run tasks and do not store data in HDFS

EMR comes bundled with Spark, HBase, Presto, Hive, Flink... 
When launching a cluster, it performs bootstrap actions to install custom software and applications. When the cluster is in running state, we can submit work to it. Work includes a set of steps. The cluster can auto terminate at the end of the last step.

We can submit one or more ordered steps to an Amazon EMR cluster. Each step is a unit of work that contains instructions to manipulate data for processing by software installed on the cluster.

For auto scaling of the task nodes, it uses Spot instances. Master nodes should be on Reserved Instances.

### EMR cluster Use cases

* Big data analytics: what-if analysis using statistical algorithms and predictive models to uncover hidden patterns, correlations, market trends...
* Scalable data pipelines: process it at petabyte scale.
* Real-time data streams: to create long-running, highly available, and fault-tolerant streaming data pipelines.
* Analyze data and ML adoption.

AWS Lake Formation integrates with Amazon EMR to set up, secure, and manage data lakes. You can use Lake Formation permissions together with the AWS Glue Data Catalog to provide fine-grain, column-level access to the data lake. Jobs that we submit with Amazon EMR steps can use job-centric runtime roles to access AWS resources, such as objects in Amazon S3.

### Getting Started EMR/EC2

See the [getting started tutorial](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-gs.html) with Spark, PySpark scripts stored in S3 (details below). 

???- info "Tutorial"
    The Python code and data sets are in the folder: [labs/analytics/emr-starting](https://github.com/jbcodeforce/yarkba/tree/main/labs/analytics/emr-starting). The goal is to process food establishment inspection data.

    * Create a cluster using the script `create-cluster.sh` (it uses `aws emr create-cluster` command).
    * Unzip data sources in a S3 bucket (e.g. `s3://jb-data-set/restaurants/`)
    * In the console, once the cluster is in waiting mode, add a **Step** with Spark Application, in cluster deployment mode, 

        ![](./images/emr-spark-app.png)

        Or run `deploy-app.sh` (it uses `aws emr add-steps` command).

    * The results looks like

        ```csv
        name,total_red_violations
        SUBWAY,322
        T-MOBILE PARK,315
        WHOLE FOODS MARKET,299
        ...
        ```

For other EMR examples see [the playground](../playground/spark-emr.md) and [Spark Studies](https://jbcodeforce.github.io/spark-studies/).

See [Pricing](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-gs.html) based on EC2 type and region.

## [EMR Serverless](https://us-west-2.console.aws.amazon.com/emr/home?region=us-west-2#/serverless)

The newest and easiest way for data analysts and engineers to run open-source big data analytics frameworks without configuring, managing, and scaling clusters and servers.

End users work from EMR Studio using notebooks, but we can also submit jobs via APIs and CLI. 

It uses the concept of applications to keep configurations and metadata. A job is a request submitted to an Amazon EMR Serverless application that runs asynchronously and is tracked through completion. Jobs are run in a single Availability Zone to avoid cross-AZ network communication. In the figure below the green layer is owned by the user, with data in S3, while the orange layer is managed by AWS. Spark or Hive engines run jobs on the data coming from S3 (in fact data can come from a lot of different data sources). 

![](./diagrams/emr-serverless.drawio.png){ width=900 }

No need to right-size clusters for varying jobs and data sizes. It automatically adds and removes workers at different stages of the job. EMR is charged for aggregated vCPU, memory, and storage resources used from the time a worker starts running until it stops.

* We can submit jobs using workflow orchestration services like AWS Step Functions, Apache Airflow, or AWS Managed Workflows for Apache Airflow.
* Logging: By default, EMR Serverless stores application logs securely in Amazon EMR managed storage for a maximum of 30 days. Before our jobs can send log data to Amazon S3, we must allow `s3:PutObject` on the `arn:aws:s3:::.../*` s3 bucket, in the permissions policy for the job runtime role. 
* Monitoring with CloudWatch custom dashboard: See the CloudFormation definition under [lab/analytics/emr-serverless folder](https://github.com/jbcodeforce/yarkba/tree/main/labs/analytics/emr-serverless) and using the command `./defineCWdashboard.sh`, we can get a dashboard for the Serverless EMR application:

    ![](./images/emr-serverless-cw-dashboard.png)

    So we need to define one dashboard per application.

    Every minute EMR Serverless emits (CPUAllocated, IdleWorkerCount,MaxCPUAllowed) metrics at the application level and at the worker-type and capacity-allocation-type levels.


### EMR Serverless Use cases

* Spark ETL.
* Large scale SQL queries using Hive.
* Interactive analysis using Jupyter notebooks with EMR Studio.
* Analysis using Presto
* Real-time streaming data pipelines: perform fault-tolerant stream processing of live data streams using Apache Spark or Apache Flink data frameworks.
* AI/ML: pre-process data and train models and perform prediction and validation to build accurate ML models. It may use Spark MLlib, TensorFlow, and Apache MXNet. 

### EMR Serverless - Getting Started

Source is the [tutorial - getting started](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/getting-started.html). 

???- "Details"
    * We need an IAM role with a custom trust policy to enable others to perform actions in this account (see role `EMRServerlessS3RuntimeRole` and security policy `EMRServerlessS3AndGlueAccessPolicy`). 
    * Use EMR Studio and create an application. We can now use Graviton as CPU:

        ![](./images/emr-serverless-app-1.png)

    * Define the PySpark script to be used and put it in a S3 bucket. For example WordCount.py

        ```sh
        aws s3 cp s3://us-east-1.elasticmapreduce/emr-containers/samples/wordcount/scripts/wordcount.py s3://jb-data-set/scripts/
        ```

    * Define a job using the script, using the **Spark properties** of: `--conf spark.executor.cores=1 --conf spark.executor.memory=4g --conf spark.driver.cores=1 --conf spark.driver.memory=4g --conf spark.executor.instances=1`

        ![](./images/emr-serverless-app-2.png)

    * Once the job runs the status shows as `Success`, we  can view the output of the job in the S3 bucket.
    * Log should be in logs folder.
    * Delete output from s3 bucket: `aws s3 rm s3://jb-data-set/emr-serverless-spark/ --recursive`

    * **WordCount.py app with CLI:** Scripts are under [labs/analytics/emr-serverless](https://github.com/jbcodeforce/yarkba/tree/main/labs/analytics/emr-serverless)

    * If the application was not created before like in manual step above, use the following command: (which is in the script `createApplication.sh`) 

        ```sh
        aws emr-serverless create-application --release-label emr-6.8.0 --type "SPARK"  --name My_First_Application
        ```

    * Get the application ID: `./getApplicationId.sh My_First_Application`
    * Be sure to have the wordcount.py in the scripts folder in s3 bucket

        ```sh
        aws s3 cp s3://us-east-1.elasticmapreduce/emr-containers/samples/wordcount/scripts/wordcount.py s3://DOC-EXAMPLE-BUCKET/scripts/
        ```

    * Get the role ARN 

        ```sh
        aws iam list-roles | jq -r '.Roles[] | select(.RoleName=="EMRServerlessS3RuntimeRole") | .Arn '
        ```

    * Submit the job:  `./submitJob.sh`. The submission output looks like:

        ```json
        {
        "applicationId": "00f6b0eou5biqd0l",
        "jobRunId": "00f6b25bek7v3f0l",
        "arn": "arn:aws:emr-serverless:us-west-2:....:/applications/00f6b0eou5biqd0l/jobruns/00f6b25bek7v3f0l"
        }
        ```

## [EMR on EKS](https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/emr-eks.html)

Advantages:

* Run with other workload deployed on EKS. Fully managed lifecycle of the EMR jobs.
* 3x faster performance.
* Improves resource utilization and simplifies infrastructure management across multiple Availability Zones.
* Deploy in seconds instead of minutes.
* Centrally manage a common computing platform to consolidate EMR workloads with other apps. Access to built-in monitoring and logging functionality.
* Reduce operational overhead with automated Kubernetes cluster management and OS patching

![](https://docs.aws.amazon.com/images/emr/latest/EMR-on-EKS-DevelopmentGuide/images/emr-on-eks-architecture.png)

* Amazon EMR uses virtual clusters to run jobs and host endpoints. A virtual cluster is a Kubernetes namespace that Amazon EMR is registered with. 

### Deployment and setup

* [Prepare a EKS cluster](../serverless/eks.md)
* Amazon EMR on EKS needs CoreDNS for running jobs on EKS cluster. So update CoreDNS if needed.
* [Enable cluster access for Amazon EMR on EKS](https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/setting-up-cluster-access.html) to a specific namespace by creating a k8s role, role binding to a k8s user, and map this user to the service linked role `AWSServiceRoleForAmazonEMRContainers`.
* [Enable IAM Roles for Service Accounts (IRSA) on the EKS cluster](https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/setting-up-enable-IAM.html) by creating an OIDC identity provider
* Create a job execution role

## Deeper dive

* [EKS workshop with EMR](https://www.eksworkshop.com/advanced/430_emr_on_eks/)
* [Blog Run Big Data Applications without Managing Servers ](https://aws.amazon.com/blogs/big-data/announcing-amazon-emr-serverless-preview-run-big-data-applications-without-managing-servers/)


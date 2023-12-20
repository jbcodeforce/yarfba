# Cost Optimization

## Resource tagging

Use [cost allocation tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html) to track cost in reports. User-defined tags use the `user:` prefix, and the AWS-generated tag uses the `aws:`.

Need to activate the tags in Billing and Cost console. 

The `awsApplication` tag will be automatically added to all resources that are associated with applications that are set up in AWS Service Catalog AppRegistry.

## Budgets

Create a budget and send alarms when costs exceed the budget. We can use 4 types of budget: Usage, Cost, Reservation and Saving Plans.

Budget Actions can run action on our behalf when a budget exceeds cost or usage threshold. Actions can be to apply an IAM policy to a user, group or role, to apply a Service Control Policy to an Organization Unit, or stop EC2 or RDS instances.

Actions can be automatic or use a human workflow approval process.

## [Cost Explorer](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html)

Tool to view and analyze our costs and usage.

## [Trusted Advisor](https://docs.aws.amazon.com/awssupport/latest/user/trusted-advisor.html)

Trusted Advisor inspects our AWS environment, and then makes recommendations when opportunities exist for cost optimization, security, fault tolerance, performance, and service limits. Inspect all resources cross regions and aggregates are computed once a week. For full checks account needs to be in business or enterprise support plans. Check results can be consumed into CloudWatch. Priority helps us focus on the most important recommendations to optimize the cloud deployments, improve resilience, and address security gaps.

The implication of the check will depend of the check type. Some of the items could be excluded.

Example of check could be `low utilization of EC2 instances` when daily CPU was 10% or less in the last 14 days.

User can filter out recommendations by resource tag, and can also exclude items. The Support API can be used to get check reports.

The [list of checks performed](https://docs.aws.amazon.com/awssupport/latest/user/trusted-advisor-check-reference.html).

TA cannot check for S3 object that are public inside a bucket, but can check if S3 bucket is public.

## [Service Quotas](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html)

Service Quotas is an AWS service that helps you manage your quotas (also known as limits) for many AWS services in one location. Along with looking up the quota values and current utilization, you can request a quota increase from the Service Quotas console.

## Saving plans

New pricing plan to get discount. Commit to certain type of machine, on a specific region and usage. Anything above the usage will be billed with on-demand price. 

* EC2 Instance Saving plan is flexible for the size, (large, XLarge...), OS and tenancy.
* Compute savings plan let change the instance family, region, compute type, OS and tenancy. It is like a convertible RI.

## [AWS Compute Optimizer](https://docs.aws.amazon.com/compute-optimizer/latest/ug/what-is-compute-optimizer.html)

AWS Compute Optimizer allows to automate the collection of metrics for under-utilized and under-performing compute instances. It can then generate recommendations for you to save money.

If we need to get Memory utilization, we need to deploy EC2 Cloudwatch agent to report on memory metrics to CloudWatch.

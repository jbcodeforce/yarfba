

awslocal stepfunctions update-state-machine --definition "$(jq -Rs '.' ./statemachine/credit_approval.asl.json)" --state-machine-arn arn:aws:states:us-west-2:000000000000:stateMachine:step-sol-1-CreditApprovalProcessFlo-47aab0bf
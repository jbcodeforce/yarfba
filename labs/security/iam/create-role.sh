aws iam create-role \
    --role-name SupportRole \
    --assume-role-policy-document file://Support-Role-Trust-Policy.json \
    --max-session-duration 7200

aws iam   attach-role-policy --role-name SupportRole \
    --policy-arn arn:aws:iam::aws:policy/job-function/SupportUser
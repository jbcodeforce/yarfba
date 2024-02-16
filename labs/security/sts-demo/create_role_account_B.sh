aws iam create-role \
    --role-name access-demo \
    --assume-role-policy-document file://Support-Role-Trust-Policy.json \
    --max-session-duration 7200


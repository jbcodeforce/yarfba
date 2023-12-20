
Based on the [ABAC tutorial](https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_attribute-based-access-control.html)

- 2 projects: pegasus and unicorn
- 2 user groups: engineering and Quality Assurance
- different resources

1. Get a session token for an admin user of the account do the following steps
1. Create a policy to allow a user to assume any role in your account with the `access-` name prefix.
1. Create 4 users part of the engineering or QA team for the two projects: unicorn and pegasus
1. Create 4 roles to be assumed by each person
1. Keep account admin session open
1. Start incognito web browser, login as `access-Arnav-peg-eng` user, try to access the Secret Manager: >> "You don't have permission to view or select from existing secrets in your account. Contact your administrator to obtain ListSecrets access.". Swith role to use `access-uni-engineering`.
1. Go to create a secret. Add the secret named: `test-access-peg-eng` with key: `test-access-key` and value: `test-access-secret`, and the good tags to be able to create the tag matching the logged user: 

    | Key | Value |
    | --- | --- |
    | access-team |	eng |
    | access-project |	peg |
    | cost-center | 987654 |
    | Name | Jane |

1. Create the other secrets
1. The policy that we attached to each role allows the employees to view any secrets tagged with their team name, regardless of their project. Select one of the user and 
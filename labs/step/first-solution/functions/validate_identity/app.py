import re

def lambda_handler(event, context):
    email_validate_pattern = r"^\S+@\S+\.\S+$"
    if re.match(email_validate_pattern, event['email']):
        event['identity_validated'] = True
    else:
        event['identity_validated'] = False
    return event


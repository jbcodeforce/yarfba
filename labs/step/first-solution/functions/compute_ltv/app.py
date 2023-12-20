from random import randint


def lambda_handler(event, context):
    """
    Parameters
    ----------
    event: dict, required
        Input event to the Lambda function

    context: object, required
        Lambda Context runtime methods and attributes

    Returns
    ------
        a value for the load to value
    """
    loan_amount = event['ammount']
    property = event['property_value']
    event['LTV'] = loan_amount / property * 100
    return event


from random import randint


def lambda_handler(event, context):
    """
    Parameters
    ----------
    event:  loan application with LTV

    context: object, required
        Lambda Context runtime methods and attributes

    Returns
    ------
       
    """
    scores = [700, 820, 640, 460, 726, 850, 694, 721, 556]
    idx= randint(0, len(scores)-1)
    event['credit_score'] = scores[idx]
    return event

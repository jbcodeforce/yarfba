
def lambda_handler(event, context):
      address = event['address']
      fields = ['street', 'city', 'state', 'zip']
      error = False
      for field in fields:
        if field not in address:
            error = True
        elif len(address[field]) == 0:
            error = True
      event['address_validated'] = not error
      return event


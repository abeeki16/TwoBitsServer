import plaid
import os
import datetime
from testing_variables import SANDBOX_INSTITUTION
from secret import PLAID_CLIENT_ID, PLAID_SECRET, PLAID_PUBLIC_KEY, PLAID_PRODUCTS, \
    PLAID_COUNTRY_CODES, PLAID_ENV


PLAID_ACCESS_TOKEN = None
PLAID_PUBLIC_TOKEN = None


def get_client():
    client = plaid.Client(client_id = PLAID_CLIENT_ID,
                          secret = PLAID_SECRET,
                          public_key = PLAID_PUBLIC_KEY,
                          environment = PLAID_ENV,
                          api_version = '2019-05-29')
    return client


def get_access_token(client):
    public_token = client.Sandbox.public_token.create(SANDBOX_INSTITUTION, ['transactions'])
    # the public token is received from Plaid Link
    response = client.Item.public_token.exchange(public_token)
    global access_token
    access_token = response['access_token']
    try:
        exchange_response = client.Item.public_token.exchange(public_token)
    except plaid.errors.PlaidError as e:
        return e  #jsonify(format_error(e))
    access_token = exchange_response['access_token']
    return exchange_response


def get_transactions(client):
    """ Returns transactions for the past 30 days."""
    start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-30))
    end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())
    try:
        transactions_response = client.Transactions.get(access_token, start_date, end_date)
    except plaid.errors.PlaidError as e:
        return e, False  #jsonify(format_error(e))
    return transactions_response, True


def roundup(transaction, user_bits):
    """Rounding up individual transaction based on user_bits choice"""
    twobits = 0.25
    to_donate = twobits - transaction % twobits
    if user_bits > 2:
        to_donate += (user_bits*0.125) - 0.25
    return round(to_donate, 2)


def get_monthly_roundup_charge():
    """Returns total sum of rounded up transactions for the past 30 days."""
    client = get_client()
    transaction_response, success = get_transactions(client)
    if success == False:
        return None
    transactions = transaction_response['transactions']
    total_sum = 0
    for transaction in transactions:
        if transaction['amount'] > 0:
            total_sum += roundup(transaction['amount'], 2)
    return total_sum


def format_error(e):
  return {'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type, 'error_message': e.message } }


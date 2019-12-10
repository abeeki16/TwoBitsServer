import plaid
import datetime
from secret import PLAID_CLIENT_ID, PLAID_SECRET, PLAID_PUBLIC_KEY, PLAID_PRODUCTS, \
    PLAID_COUNTRY_CODES, PLAID_ENV, SANDBOX_INSTITUTION
from plaid import Client as PlaidClient

PLAID_ACCESS_TOKEN = None
PLAID_PUBLIC_TOKEN = None

## for testing purposes
def create_plaid_client():
    '''Create a new client for testing.'''
    return PlaidClient(PLAID_CLIENT_ID,
                  PLAID_SECRET,
                  PLAID_PUBLIC_KEY,
                  'sandbox',
                  api_version="2019-05-29")


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
    return access_token


def get_transactions(client, access_token):
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


def get_monthly_roundup_charge(client):
    access_token = get_access_token(client)
    """Returns total sum of rounded up transactions for the past 30 days."""
    transaction_response, success = get_transactions(client, access_token)

    if success == False:
        return None
    transactions = transaction_response['transactions']
    total_sum = 0
    for transaction in transactions:
        if transaction['amount'] > 0:
            total_sum += roundup(transaction['amount'], 2)
    return total_sum
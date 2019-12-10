import math
import os
import datetime
import stripe
from plaid import Client as PlaidClient
from secret import STRIPE_LIVE_PUBLIC_KEY, STRIPE_LIVE_SECRET_KEY, STRIPE_PUBLIC_KEY_TEST, \
    STRIPE_SECRET_KEY_TEST, STRIPE_LIVE_MODE, STRIPE_TEST_API_KEY
from secret import PLAID_CLIENT_ID, PLAID_SECRET, PLAID_PUBLIC_KEY, PLAID_PRODUCTS, \
    PLAID_COUNTRY_CODES, PLAID_ENV, SANDBOX_INSTITUTION
import plaid
from plaid_handler import create_plaid_client, get_monthly_roundup_charge


public_token = 'public-sandbox-a0d63f62-4b92-4fb3-a6d3-a0db9fad3011'


def create_client():
    '''Create a new client for testing.'''
    return PlaidClient(PLAID_CLIENT_ID,
                  PLAID_SECRET,
                  PLAID_PUBLIC_KEY,
                  'sandbox',
                  api_version="2019-05-29",
                  client_app="plaid-python-unit-tests")


SANDBOX_INSTITUTION = 'ins_109508'
SANDBOX_INSTITUTION_NAME = 'First Platypus Bank'

SANDBOX_INSTITUTIONS = [
    'ins_109508',
    'ins_109509',
    'ins_109510',
    'ins_109511',
    'ins_109512',
]

def register_stripe_user():
    """Create Stripe customer"""
    client = PlaidClient(client_id = PLAID_CLIENT_ID,
                         secret = PLAID_SECRET,
                         public_key = PLAID_PUBLIC_KEY,
                         environment = PLAID_ENV)

    # exchange_token_response is obtained from the Client-side aka front-end
    exchange_token_response = client.Item.public_token.exchange(public_token)

    access_token = exchange_token_response['access_token']
    response = client.Accounts.get(access_token)
    assert response['accounts'] is not None

    print("response:", response)
    account_id = response['accounts'][0]['account_id']

    access_token = exchange_token_response['access_token']

    stripe_response = client.Processor.stripeBankAccountTokenCreate(access_token, account_id)
    bank_account_token = stripe_response['stripe_bank_account_token']
    print(bank_account_token)

    return True

# register_stripe_user()


def stripe_client():
    client = create_client()

    exchange_token_response = client.Item.public_token.exchange('[Plaid Link public_token]')
    access_token = exchange_token_response['access_token']
    stripe_response = client.Processor.stripeBankAccountTokenCreate(access_token, '[Account ID]')
    bank_account_token = stripe_response['stripe_bank_account_token']
    return bank_account_token


def test_stripe_processor_token():
    client = create_client()
    # Just test the failure case - behavior here depends on the API keys used
    client.Processor.stripeBankAccountTokenCreate('fakeAccessToken', 'fakeAccountId')


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




def setup_subscription():
    """Setup user for monthly subscription charges."""
    customer_id = 'cus_GCo7Uo3OplKoZh'
    # client = get_client()
    ########

    stripe.api_key = "sk_test_PpdcRckmBiDlfwQLDo2JEWe800dvTkhyP1"
    monthly = 100000

    plan = stripe.Plan.create(
        amount = monthly,
        currency = "usd",
        interval = "month",
        product = {"name": "Gold special"},
    )
    plan_id = plan['id']

    product = stripe.Product.create(
        name = "2Bits Monthly donation",
        type = "service",
    )
    product_id = product['id']

    #Creates a new subscription on an existing customer.
    subscription = stripe.Subscription.create(
        customer = customer_id,
        items = [{"plan": plan_id}],
    )

    subscription_id = subscription['id']
    print(stripe.Plan.retrieve(plan_id))
    print(monthly, subscription_id)


setup_subscription()
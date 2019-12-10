from secret import STRIPE_LIVE_PUBLIC_KEY, STRIPE_LIVE_SECRET_KEY, STRIPE_PUBLIC_KEY_TEST, \
    STRIPE_SECRET_KEY_TEST, STRIPE_LIVE_MODE, STRIPE_TEST_API_KEY
import math
from plaid.errors import InvalidRequestError
import stripe
import plaid
from plaid_handler import create_plaid_client, get_monthly_roundup_charge

# public token retrieved from Client-Side.
public_token = 'public-sandbox-04e9c869-623e-4093-b4de-a4fc8cb665a8'
plaid_access_token = public_token

##For testing purposes
def create_stripe_client():
    """Create Stripe customer"""
    return create_plaid_client()

'''
To fix:
"the provided API keys are not enabled for the Stripe ACH integration. 
please see https://plaid.com/docs/link/stripe for more information."
We need signed Stripe+Plaid form.
'''
def obtain_tokens(client):
    # exchange_token_response is obtained from the Client-side aka front-end
    exchange_token_response = client.Item.public_token.exchange(public_token)
    access_token = exchange_token_response['access_token']
    plaid_access_token = access_token
    response = client.Accounts.get(access_token)
    assert response['accounts'] is not None
    print("response:", response)
    account_id = response['accounts'][0]['account_id']
    stripe_response = client.Processor.stripeBankAccountTokenCreate(access_token, account_id)
    bank_account_token = stripe_response['stripe_bank_account_token']
    return


def stripe_client():
    client = create_plaid_client()

    exchange_token_response = client.Item.public_token.exchange('[Plaid Link public_token]')
    access_token = exchange_token_response['access_token']

    stripe_response = client.Processor.stripeBankAccountTokenCreate(access_token, '[Account ID]')
    bank_account_token = stripe_response['stripe_bank_account_token']
    return bank_account_token



def setup_subscription():
    """Setup user for monthly subscription charges."""
    client = create_stripe_client()
    ########
    customer_id = 'cus_GCo7Uo3OplKoZh'

    monthly = get_monthly_roundup_charge(client)

    print(monthly)

    stripe.api_key =STRIPE_TEST_API_KEY


    plan = stripe.Plan.create(
        amount = "10000",
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
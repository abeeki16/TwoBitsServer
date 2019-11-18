from plaid_handler import get_client
from secret import STRIPE_LIVE_PUBLIC_KEY, STRIPE_LIVE_SECRET_KEY, STRIPE_TEST_PUBLIC_KEY, \
    STRIPE_TEST_SECRET_KEY, STRIPE_LIVE_MODE, DJSTRIPE_WEBHOOK_SECRET
import stripe
import os



def stripe_client():
    client = get_client()
    exchange_token_response = client.Item.public_token.exchange('[Plaid Link public_token]')
    access_token = exchange_token_response['access_token']

    stripe_response = client.Processor.stripeBankAccountTokenCreate(access_token, '[Account ID]')
    bank_account_token = stripe_response['stripe_bank_account_token']


def setup_subscription():
    """Setup user for monthly subscription charges."""
    client = get_client()

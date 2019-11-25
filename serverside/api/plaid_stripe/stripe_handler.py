from plaid_handler import get_client
from secret import STRIPE_LIVE_PUBLIC_KEY, STRIPE_LIVE_SECRET_KEY, STRIPE_TEST_PUBLIC_KEY, \
    STRIPE_TEST_SECRET_KEY, STRIPE_LIVE_MODE, DJSTRIPE_WEBHOOK_SECRET
from testing_variables import STRIPE_API_KEY
import stripe
from api.models import Profile


def register_stripe_user(current_user):
    """Create Stripe customer"""
    stripe.Customer.create(
        email = 'jenny.rosen@example.com',
        payment_method = 'pm_1FWS6ZClCIKljWvsVCvkdyWg',
        invoice_settings = {
            'default_payment_method': 'pm_1FWS6ZClCIKljWvsVCvkdyWg',
        },
    )

    customer = stripe.Customer.create(
        email=current_user.email,
        source=stripe.request.form['stripeToken'],
        )

    # donator = Donator(
    #     customer_id=customer.id,
    #     user_id=current_user.id
    #     )

    # db.session.add(donator)
    # db.session.commit()
    return True


def stripe_client():
    client = get_client()
    exchange_token_response = client.Item.public_token.exchange('[Plaid Link public_token]')
    access_token = exchange_token_response['access_token']

    stripe_response = client.Processor.stripeBankAccountTokenCreate(access_token, '[Account ID]')
    bank_account_token = stripe_response['stripe_bank_account_token']
    return bank_account_token

def subscription_product():
    pass



def setup_subscription():
    """Setup user for monthly subscription charges."""
    client = get_client()
    pass


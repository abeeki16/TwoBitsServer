import os

"""In order to run the app, you have to be registered PLAID and STRIPE developer, 
and have required keys stored on your running machine environment."""


PLAID_CLIENT_ID = os.environ.get("STRIPE_LIVE_PUBLIC_KEY")
PLAID_SECRET = os.environ.get("PLAID_SECRET")
PLAID_PUBLIC_KEY = os.environ.get("PLAID_PUBLIC_KEY")
PLAID_PRODUCTS = "transactions"
PLAID_COUNTRY_CODES = "US"
PLAID_ENV = "sandbox"

STRIPE_LIVE_PUBLIC_KEY = os.environ.get("STRIPE_LIVE_PUBLIC_KEY")
STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY")
STRIPE_PUBLIC_KEY_TEST = os.environ.get("STRIPE_PUBLIC_KEY_TEST")
STRIPE_SECRET_KEY_TEST = os.environ.get("STRIPE_SECRET_KEY_TEST")
STRIPE_LIVE_MODE = False  # Change to True in production
STRIPE_TEST_API_KEY = os.environ.get("STRIPE_SECRET_KEY_TEST")
# Get it from the section in the Stripe dashboard where you added the webhook endpoint
DJSTRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK","whsec_xxx")



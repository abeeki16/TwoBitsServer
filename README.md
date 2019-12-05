# TwoBits Donations
Mobile Application

Project repository for the CS591 X-Lab Practicum. <br />
Fall 2019, Boston University.

## Team members (alphabetically ordered)
* [Ajit Beeki](https://github.com/abeeki16)
* [Camilla Satte](https://github.com/collisior)
* [Kaylin Mok](https://github.com/mhkaylyn)
* [Will Munoz](https://github.com/WillPower98)


## Technologies

* Backend: Django (Python-based framework), some parts are handled in Android Studio
* Frontend: Java, XML (Android Studio)
* Database: SQLite


## Want to run the project?

1. Set your environment variables
To gain access to the Plaid API, please create an account on [Plaid's Dashboard](https://dashboard.plaid.com/signin). 
To gain access to the STRIPE API, please create an account on [Stripe's Dashboard](https://dashboard.stripe.com/login). 
Once you’ve completed the signup process, then change your environment values by entering in terminal prompt:

```
$ vim ~/.bash_profile
```

and set these values: PLAID_CLIENT_ID, PLAID_SECRET, PLAID_PUBLIC_KEY, STRIPE_API_KEY, STRIPE_LIVE_PUBLIC_KEY, STRIPE_LIVE_SECRET_KEY, STRIPE_PUBLIC_KEY_TEST, STRIPE_SECRET_KEY_TEST, STRIPE_LIVE_MODE = False, STRIPE_TEST_API_KEY

2. Open up your terminal prompt app and go to the desired folder to clone the repo. Then enter:

```
$ git clone https://github.com/abeeki16/TwoBitsServer.git
$ git clone https://github.com/collisior/TwoBits.git
$ pip install -r requirements.txt
$ cd serverside
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

2. Open TwoBits project using [Android Studio](https://developer.android.com/studio/install). Build and Run the app.




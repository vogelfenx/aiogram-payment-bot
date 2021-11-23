import dotenv

secrets = dotenv.dotenv_values('.secrets', verbose=True,)
if not secrets:
    exit('Verify .secrets file which should be located in root dir')

TELEGRAM_API_TOKEN = secrets['TELEGRAM_API_TOKEN']
YOOKASSA_TEST_PAYMENT_TOKEN = secrets['YOOKASSA_TEST_PAYMENT_TOKEN']

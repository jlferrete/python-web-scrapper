import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv('LOGIN_USER')
PWD = os.getenv('LOGIN_PWD')
WEB_URL_TO_SCRAPE = os.getenv('WEB_URL_TO_SCRAPE')
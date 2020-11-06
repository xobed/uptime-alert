import os
import time
from datetime import datetime, timedelta
from typing import List

import requests
import sentry_sdk
from sentry_sdk import capture_exception

SENTRY_DSN = os.environ.get('SENTRY_DSN', default=None)
if SENTRY_DSN is None:
    raise Exception('SENTRY_DSN environment variable must be configured')

sentry_sdk.init(
    dsn=SENTRY_DSN,
)

urls_string = os.environ.get('MONITORED_URLS', default=None)
no_urls_message = 'No URLs configured. Set MONITORED_URLS environment variables with comma delimited list of URLs'

if urls_string is None:
    raise Exception(no_urls_message)

urls: List = urls_string.split(',')
if len(urls) == 0:
    raise Exception(no_urls_message)

retry_limit_seconds = int(os.environ.get('RETRY_LIMIT_SECONDS', default=60))


def check_url(url_to_check: str):
    response = requests.get(url_to_check, timeout=10)
    response.raise_for_status()
    print(f'{url_to_check} check passed')


def check_with_retry(url_to_check: str):
    timeout = datetime.now() + timedelta(seconds=retry_limit_seconds)
    wait_between_retries = 5

    while datetime.now() < timeout:
        try:
            check_url(url_to_check)
            return
        except Exception:
            if datetime.now() < timeout:
                time.sleep(wait_between_retries)

    check_url(url_to_check)


for url in urls:
    try:
        check_with_retry(url)
    except Exception as ex:
        short_message = f'URL {url} is not responding'
        message = f'{short_message}: {ex}'
        print(message)
        capture_exception(Exception(short_message))

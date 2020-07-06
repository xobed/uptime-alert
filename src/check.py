import logging
import os
from typing import List

import requests
import sentry_sdk
from sentry_sdk import capture_exception
from tenacity import stop_after_delay, retry, wait_fixed

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

retry_limit_seconds = os.environ.get('RETRY_LIMIT_SECONDS', default=60)


@retry(stop=stop_after_delay(retry_limit_seconds), wait=wait_fixed(5))
def check_url(url_to_check: str):
    response = requests.get(url_to_check)
    response.raise_for_status()
    logging.info(f'{url} check passed')


for url in urls:
    try:
        check_url(url)
    except Exception as ex:
        message = f'URL {url} is not responding: {ex}'
        capture_exception(Exception(message, ex))

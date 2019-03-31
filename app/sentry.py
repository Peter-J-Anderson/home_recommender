#!/usr/bin/env python
import os
import sentry_sdk
from sentry_sdk import configure_scope


def setup_sentry():
    sentry_sdk.init(os.environ['SENTRY_DSN'])
    with configure_scope() as scope:
        scope.user = {
            "username": r'{}\{}'.format(os.environ['USERDOMAIN'],os.environ['USERNAME']),
            "computername": r'{}'.format(os.environ['COMPUTERNAME'])
        }
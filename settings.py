import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
GOOGLEADS_YAML_FILE = os.path.join(ROOT_DIR, 'googleads.yaml')

# A string describing the order
DFP_ORDER_NAME = None

# TODO: fetch IDs programmatically so the settings are easier to configure.
# https://github.com/googleads/googleads-python-lib/blob/master/examples/dfp/v201702/company_service/get_advertisers.py
# https://github.com/googleads/googleads-python-lib/blob/master/examples/dfp/v201702/user_service/get_all_users.py

# The email of the DFP user who will be the trafficker for
# the created order
DFP_USER_EMAIL_ADDRESS = None

# Integer from DFP
DFP_ORDER_ADVERTISER_ID = None

# Integer from DFP
DFP_ORDER_TRAFFICKER_ID = None


# Try importing local settings, which will take precedence.
try:
    from local_settings import *
except ImportError:
    pass

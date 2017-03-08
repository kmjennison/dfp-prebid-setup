import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
GOOGLEADS_YAML_FILE = os.path.join(ROOT_DIR, 'googleads.yaml')


#########################################################################
# DFP SETTINGS
#########################################################################

# A string describing the order
DFP_ORDER_NAME = None

# The email of the DFP user who will be the trafficker for
# the created order
DFP_USER_EMAIL_ADDRESS = None

# The exact name of the DFP advertiser for the created order
DFP_ADVERTISER_NAME = None

# Names of placements the line items should target.
DFP_TARGETED_PLACEMENT_NAMES = []

# Sizes of placements. These are used to set line item and creative sizes.
DFP_PLACEMENT_SIZES = [
  {
    'width': '300',
    'height': '250'
  },
  {
    'width': '728',
    'height': '90'
  },
]

# Whether we should create the advertiser in DFP if it does not exist.
# If False, the program will exit rather than create an advertiser.
DFP_CREATE_ADVERTISER_IF_DOES_NOT_EXIST = False

# If settings.DFP_ORDER_NAME is the same as an existing order, add the created 
# line items to that order. If False, the program will exit rather than
# modify an existing order.
DFP_USE_EXISTING_ORDER_IF_EXISTS = False

#########################################################################
# PREBID SETTINGS
#########################################################################

PREBID_BIDDER_CODE = None

# Price buckets. This should match your Prebid settings for the partner. See:
# http://prebid.org/dev-docs/publisher-api-reference.html#module_pbjs.setPriceGranularity
# FIXME: this should be an array of buckets. See:
# https://github.com/prebid/Prebid.js/blob/8fed3d7aaa814e67ca3efc103d7d306cab8c692c/src/cpmBucketManager.js
PREBID_PRICE_BUCKETS = {
  'precision': 2,
  'min' : 0,
  'max' : 20,
  'increment': 0.10,
}

#########################################################################
# EXTRA SETTINGS
# These are not required for typical use. Only set these if you are
# directly calling some modules.
#########################################################################

DFP_ORDER_ADVERTISER_ID = None
DFP_ORDER_TRAFFICKER_ID = None

#########################################################################

# Try importing local settings, which will take precedence.
try:
    from local_settings import *
except ImportError:
    pass

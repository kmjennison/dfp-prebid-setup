
import logging
import os
import pprint

from googleads import ad_manager

from dfp.client import get_client

import settings


logger = logging.getLogger(__name__)

def create_creatives(creatives):
  """
  Creates creatives in DFP.

  Args:
    creatives (arr): an array of objects, each a creative configuration
  Returns:
    an array: an array of created creative IDs
  """
  dfp_client = get_client()
  creative_service = dfp_client.GetService('CreativeService',
    version='v201811')
  creatives = creative_service.createCreatives(creatives)

  # Return IDs of created line items.
  created_creative_ids = []
  for creative in creatives:
    created_creative_ids.append(creative['id'])
    logger.info(u'Created creative with name "{name}".'.format(name=creative['name']))
  return created_creative_ids

def create_creative_config(name, advertiser_id):
  """
  Creates a creative config object.

  Args:
    name (str): the name of the creative
    advertiser_id (int): the ID of the advertiser in DFP
  Returns:
    an object: the line item config
  """

  snippet_file_path = os.path.join(os.path.dirname(__file__),
    'creative_snippet.html')
  with open(snippet_file_path, 'r') as snippet_file:
      snippet = snippet_file.read()

  # Determine what bidder params should be
  bidder_code = getattr(settings, 'PREBID_BIDDER_CODE', None)
  bidder_params = getattr(settings, 'PREBID_BIDDER_PARAMS', None)
  hb_adid_key = 'hb_adid'

  if bidder_params is True:
    hb_adid_key += '_' + bidder_code

    if len(hb_adid_key) > 20:
      hb_adid_key = hb_adid_key[:20]

  snippet = snippet.replace('{hb_adid_key}', hb_adid_key)

  # https://developers.google.com/doubleclick-publishers/docs/reference/v201802/CreativeService.Creative
  config = {
    'xsi_type': 'ThirdPartyCreative',
    'name': name,
    'advertiserId': advertiser_id,
    'size': {
      'width': '1',
      'height': '1'
    },
    'snippet': snippet,
    # https://github.com/prebid/Prebid.js/issues/418
    'isSafeFrameCompatible': False,
  }

  return config

def build_creative_name(bidder_code, order_name, creative_num):
    """
    Returns a name for a creative.

    Args:
      bidder_code (str): the bidder code for the header bidding partner
      order_name (int): the name of the order in DFP
      creative_num (int): the num_creatives distinguising this creative from any
        duplicates
    Returns:
      a string
    """
    return '{bidder_code}: HB {order_name}, #{num}'.format(
        bidder_code=bidder_code, order_name=order_name, num=creative_num)

def create_duplicate_creative_configs(bidder_code, order_name, advertiser_id,
  num_creatives=1):
  """
  Returns an array of creative config object.

  Args:
    bidder_code (str): the bidder code for the header bidding partner
    order_name (int): the name of the order in DFP
    advertiser_id (int): the ID of the advertiser in DFP
    num_creatives (int): how many creative configs to generate
  Returns:
    an array: an array of length `num_creatives`, each item a line item config
  """
  creative_configs = []
  for creative_num in range(1, num_creatives + 1):
    config = create_creative_config(
      name=build_creative_name(bidder_code, order_name, creative_num),
      advertiser_id=advertiser_id,
    )
    creative_configs.append(config)
  return creative_configs


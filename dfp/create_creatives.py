
import logging
import os
import pprint

from googleads import dfp

from dfp.client import get_client


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
    version='v201702')
  creatives = creative_service.createCreatives(creatives)

  # Return IDs of created line items.
  created_creative_ids = []
  for creative in creatives:
    created_creative_ids.append(creative['id'])
    logger.info('Created creative with ID "{0}" and name "{1}".'.format(
      creative['id'], creative['name']))
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

  # https://developers.google.com/doubleclick-publishers/docs/reference/v201702/CreativeService.Creative
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

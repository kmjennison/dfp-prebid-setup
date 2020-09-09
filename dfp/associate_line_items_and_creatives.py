
import logging
from googleads import ad_manager

from dfp.client import get_client


logger = logging.getLogger(__name__)

def make_licas(line_item_ids, creative_ids, size_overrides=[]):
  """
  Attaches creatives to line items in DFP.

  Args:
    line_item_ids (arr): an array of line item IDs
    creative_ids (arr): an array of creative IDs
  Returns:
    None
  """
  dfp_client = get_client()
  lica_service = dfp_client.GetService(
    'LineItemCreativeAssociationService', version='v202008')

  sizes = []

  for size_override in size_overrides:
    sizes.append(size_override)

  licas = []
  for line_item_id in line_item_ids:
    for creative_id in creative_ids:
      licas.append({
        'creativeId': creative_id,
        'lineItemId': line_item_id,
        # "Overrides the value set for Creative.size, which allows the
        #   creative to be served to ad units that would otherwise not be
        #   compatible for its actual size."
        #    https://developers.google.com/doubleclick-publishers/docs/reference/v201802/LineItemCreativeAssociationService.LineItemCreativeAssociation
        #
        # This is equivalent to selecting "Size overrides" in the DFP creative
        # settings, as recommended: http://prebid.org/adops/step-by-step.html
        'sizes': sizes
      })

  batchsize = 500
  for i in range(0, len(licas), batchsize):
    batch = licas[i:i+batchsize] # select a portion of licas array to process in batches
    batch = lica_service.createLineItemCreativeAssociations(batch)

    if batch:
      current_total = i+batchsize if i+batchsize < len(licas) else len(licas)
      logger.info('Created {0} line items of {1} <> for creative associations.'.format(current_total, len(licas)))
    else:
      logger.info('No line item <> creative associations created.')
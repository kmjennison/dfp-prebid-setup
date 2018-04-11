
import logging
from googleads import dfp

from dfp.client import get_client

import settings


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
    'LineItemCreativeAssociationService', version='v201802')

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

  associations_batch = getattr(settings, 'DFP_ASSOCIATIONS_BATCH', None)

  if not associations_batch is None:
    while licas:
      batch = []
      
      for b in range(0, associations_batch):
        if licas:
          batch.append(licas.pop(0))

      batch = lica_service.createLineItemCreativeAssociations(batch)

      if batch:
        logger.info(
          u'Created {0} line item <> creative associations.'.format(len(batch)))
      else:
        logger.info(u'No line item <> creative associations created.')
  else:
    licas = lica_service.createLineItemCreativeAssociations(licas)

    if licas:
      logger.info(
        u'Created {0} line item <> creative associations.'.format(len(licas)))
    else:
      logger.info(u'No line item <> creative associations created.')


from googleads import dfp

from dfp.client import get_client


def make_licas(line_item_ids, creative_ids):
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
    'LineItemCreativeAssociationService', version='v201702')

  licas = []
  for line_item_id in line_item_ids:
    for creative_id in creative_ids:
      licas.append({'creativeId': creative_id,
                    'lineItemId': line_item_id})
  licas = lica_service.createLineItemCreativeAssociations(licas)

  if licas:
    print 'Created {0} line item <> creative associations.'.format(len(licas))
  else:
    print 'No line item <> creative associations created.'

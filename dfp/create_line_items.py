
from googleads import dfp

from dfp.client import get_client


def create_line_items(line_items):
  """
  Creates line items in DFP.

  Args:
    line_items (arr): an array of objects, each a line item configuration
  Returns:
    an array: an array of created line item IDs
  """
  dfp_client = get_client()
  line_item_service = dfp_client.GetService('LineItemService', version='v201802')
  line_items = line_item_service.createLineItems(line_items)

  # Return IDs of created line items.
  created_line_item_ids = []
  for line_item in line_items:
    created_line_item_ids.append(line_item['id'])
  return created_line_item_ids

def create_line_item_config(name, order_id, placement_ids, cpm_micro_amount,
  sizes, hb_bidder_key_id, hb_pb_key_id, hb_bidder_value_id, hb_pb_value_id,
  currency_code='USD', root_ad_unit=None):
  """
  Creates a line item config object.

  Args:
    name (str): the name of the line item
    order_id (int): the ID of the order in DFP
    placement_ids (arr): an array of DFP placement IDs to target
    cpm_micro_amount (int): the currency value (in micro amounts) of the
      line item
    sizes (arr): an array of objects, each containing 'width' and 'height'
      keys, to set the creative sizes this line item will serve
    hb_bidder_key_id (int): the DFP ID of the `hb_bidder` targeting key
    hb_pb_key_id (int): the DFP ID of the `hb_pb` targeting key
    currency_code (str): the currency code (e.g. 'USD' or 'EUR')
  Returns:
    an object: the line item config
  """

  # Set up sizes.
  creative_placeholders = []
  
  for size in sizes:
    creative_placeholders.append({
      'size': size
    })

  # Create key/value targeting for Prebid.
  # https://github.com/googleads/googleads-python-lib/blob/master/examples/dfp/v201802/line_item_service/target_custom_criteria.py
  # create custom criterias

  hb_bidder_criteria = {
    'xsi_type': 'CustomCriteria',
    'keyId': hb_bidder_key_id,
    'valueIds': [hb_bidder_value_id],
    'operator': 'IS'
  }

  hb_pb_criteria = {
    'xsi_type': 'CustomCriteria',
    'keyId': hb_pb_key_id,
    'valueIds': [hb_pb_value_id],
    'operator': 'IS'
  }

  # The custom criteria will resemble:
  # (hb_bidder_criteria.key == hb_bidder_criteria.value AND
  #    hb_pb_criteria.key == hb_pb_criteria.value)
  top_set = {
    'xsi_type': 'CustomCriteriaSet',
    'logicalOperator': 'AND',
    'children': [hb_bidder_criteria, hb_pb_criteria]
  }

  targeting = {
    'targetedPlacementIds': placement_ids
  }

  if not root_ad_unit is None:
    targeting = {
      'targetedAdUnits': [{
        'adUnitId': root_ad_unit['id'],
        'includeDescendants': True
      }]
    }

  # https://developers.google.com/doubleclick-publishers/docs/reference/v201802/LineItemService.LineItem
  line_item_config = {
    'name': name,
    'orderId': order_id,
    # https://developers.google.com/doubleclick-publishers/docs/reference/v201802/LineItemService.Targeting
    'targeting': {
      'inventoryTargeting': targeting,
      'customTargeting': top_set,
    },
    'startDateTimeType': 'IMMEDIATELY',
    'unlimitedEndDateTime': True,
    'lineItemType': 'PRICE_PRIORITY',
    'costType': 'CPM',
    'costPerUnit': {
      'currencyCode': currency_code,
      'microAmount': cpm_micro_amount
    },
    'creativeRotationType': 'EVEN',
    'primaryGoal': {
      'goalType': 'NONE'
    },
    'creativePlaceholders': creative_placeholders,
  }
  return line_item_config

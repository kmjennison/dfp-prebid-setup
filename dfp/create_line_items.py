
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
  line_item_service = dfp_client.GetService('LineItemService', version='v201702')
  line_items = line_item_service.createLineItems(line_items)

  # Return IDs of created line items.
  created_line_item_ids = []
  for line_item in line_items:
    created_line_item_ids.append(line_item['id'])
  return created_line_item_ids

def create_line_item_config(name, order_id, placement_ids, cpm_micro_amount):
  """
  Creates a line item config object.

  Args:
    name (str): the name of the line item
    order_id (int): the ID of the order in DFP
    placement_ids (arr): an array of DFP placement IDs to target
    cpm_micro_amount (int): the currency value (in micro amounts) of the
      line item
  Returns:
    an object: the line item config
  """

  # https://developers.google.com/doubleclick-publishers/docs/reference/v201702/LineItemService.LineItem
  line_item = {
    'name': name,
    'orderId': order_id,
    # https://developers.google.com/doubleclick-publishers/docs/reference/v201702/LineItemService.Targeting
    'targeting': {
      # TODO: additional key/value targeting
      'inventoryTargeting': {
        'targetedPlacementIds': placement_ids
      },
    },
    'startDateTimeType': 'IMMEDIATELY',
    'unlimitedEndDateTime': True,
    'lineItemType': 'PRICE_PRIORITY',
    'costType': 'CPM',
    'costPerUnit': {
      'currencyCode': 'USD',
      'microAmount': cpm_micro_amount
    },
    'creativeRotationType': 'EVEN',
    'primaryGoal': {
      'goalType': 'NONE'
    },
    'creativePlaceholders': [
      {
        'size': {
          'width': '1',
          'height': '1'
        },
        'size': {
          'width': '300',
          'height': '250'
        },
        'size': {
          'width': '728',
          'height': '90'
        },
      }
    ],
  }
  return line_item

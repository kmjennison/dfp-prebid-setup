
from googleads import dfp

import settings
from dfp.client import get_client
from dfp.exceptions import MissingSettingException

def create_order_config(name, advertiser_id, trafficker_id):
  """
  Creates an object of order info.
  Args:
    name (str): the name of the order
    advertiser_id (int): the ID of the advertiser in DFP
    trafficker_id (int): the ID of the DFP user owning the order
  Returns:
    an object: the order config
  """
  return {
      'name': name,
      'advertiserId': advertiser_id,
      'traffickerId': trafficker_id
  }

def main():
  """
  Create an order in DFP.

  Returns:
      None
  """

  name = getattr(settings, 'DFP_ORDER_NAME', None)
  advertiser_id = getattr(settings, 'DFP_ORDER_ADVERTISER_ID', None)
  trafficker_id = getattr(settings, 'DFP_ORDER_TRAFFICKER_ID', None)

  if name is None:
    raise MissingSettingException('DFP_ORDER_NAME')
  if advertiser_id is None:
    raise MissingSettingException('DFP_ORDER_ADVERTISER_ID')
  if trafficker_id is None:
    raise MissingSettingException('DFP_ORDER_TRAFFICKER_ID')

  dfp_client = get_client()

  orders = [
    create_order_config(name=name, advertiser_id=advertiser_id,
      trafficker_id=trafficker_id)
  ]
  order_service = dfp_client.GetService('OrderService', version='v201702')
  orders = order_service.createOrders(orders)

  # Display results.
  for order in orders:
    print ('Order with id \'%s\' and name \'%s\' was created.'
           % (order['id'], order['name']))

if __name__ == '__main__':
  main()

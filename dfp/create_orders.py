
from googleads import dfp

import settings
import dfp.get_orders
from dfp.client import get_client
from dfp.exceptions import BadSettingException, MissingSettingException


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

def create_order(order_name, advertiser_id, trafficker_id):
  """
  Creates an order in DFP.

  Args:
    order_name (str): the name of the order
    advertiser_id (int): the ID of the advertiser in DFP
    trafficker_id (int): the ID of the DFP user owning the order
  Returns:
    an object: the order config
  """

  dfp_client = get_client()

  # Check to make sure an order does not exist with this name.
  # Otherwise, DFP will throw an exception.
  existing_order = dfp.get_orders.get_order_by_name(order_name)
  if existing_order is not None:
    raise BadSettingException(('An order already exists with name {0}. '
      'Please choose a new order name.').format(order_name))

  orders = [
    create_order_config(name=order_name, advertiser_id=advertiser_id,
      trafficker_id=trafficker_id)
  ]
  order_service = dfp_client.GetService('OrderService', version='v201702')
  orders = order_service.createOrders(orders)

  order = orders[0]
  print ('Order with id \'%s\' and name \'%s\' was created.'
           % (order['id'], order['name']))

  return order['id']

def main():
  name = getattr(settings, 'DFP_ORDER_NAME', None)
  advertiser_id = getattr(settings, 'DFP_ORDER_ADVERTISER_ID', None)
  trafficker_id = getattr(settings, 'DFP_ORDER_TRAFFICKER_ID', None)

  if name is None:
    raise MissingSettingException('DFP_ORDER_NAME')
  if advertiser_id is None:
    raise MissingSettingException('DFP_ORDER_ADVERTISER_ID')
  if trafficker_id is None:
    raise MissingSettingException('DFP_ORDER_TRAFFICKER_ID')

  create_order(name, advertiser_id, trafficker_id)

if __name__ == '__main__':
  main()

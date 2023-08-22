#!/usr/bin/env python

import logging

from googleads import ad_manager

import settings
import dfp.get_orders
from dfp.client import get_client
from dfp.exceptions import BadSettingException, MissingSettingException


logger = logging.getLogger(__name__)

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
    an integer: the ID of the created order
  """

  dfp_client = get_client()

  # Check to make sure an order does not exist with this name.
  # Otherwise, DFP will throw an exception.
  existing_order = dfp.get_orders.get_order_by_name(order_name)
  if existing_order is not None:

    # If the settings allow modifying an existing order, do so. Otherwise,
    # throw an exception.
    can_use_existing_order = getattr(settings,
      'DFP_USE_EXISTING_ORDER_IF_EXISTS', None)
    if can_use_existing_order:
      order = existing_order
      logger.info(
        'Using existing order with name "{name}".'.format(name=order['name']))
    else:
      raise BadSettingException(('An order already exists with name {0}. '
        'Please choose a new order name.').format(order_name))

  # No order with the name exists, so create it.
  else:
    orders = [
      create_order_config(name=order_name, advertiser_id=advertiser_id,
        trafficker_id=trafficker_id)
    ]
    order_service = dfp_client.GetService('OrderService', version='v202305')
    orders = order_service.createOrders(orders)

    order = orders[0]
    logger.info(u'Created an order with name "{name}".'.format(name=order['name']))

  return order['id']

#!/usr/bin/env python

import logging

from googleads import ad_manager

from dfp.client import get_client


def get_order_by_name(order_name):
  """
  Gets an order by name from DFP.

  Args:
    order_name (str): the name of the DFP order
  Returns:
    a DFP order, or None
  """

  print('Getting order with order name {0}...'.format(order_name))

  client = get_client()
  order_service = client.GetService('OrderService', version='v202008')

  statement = (ad_manager.StatementBuilder()
    .Where('name = :name')
    .WithBindVariable('name', order_name))
  response = order_service.getOrdersByStatement(statement.ToStatement())

  if 'results' in response and len(response['results']) > 0:
    print('Finished fetching order.')
    return response['results'][0]
  else:
    print('Warning: no order found.')
    return None

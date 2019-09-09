#!/usr/bin/env python

import logging

from googleads import ad_manager

from dfp.client import get_client
# from tests_integration.helpers.get_order_by_name import get_order_by_name

def archive_order_by_name(order_name):
  """
  Archives an order by name in DFP.

  Args:
    order_name (str): the name of the DFP order to archive
  Returns:
    None
  """
  client = get_client()
  order_service = client.GetService('OrderService', version='v201908')

  statement = (ad_manager.StatementBuilder()
    .Where('name = :name')
    .WithBindVariable('name', order_name))
  response = order_service.performOrderAction(
    {'xsi_type': 'ArchiveOrders'},
    statement.ToStatement())

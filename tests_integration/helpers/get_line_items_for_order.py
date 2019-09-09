#!/usr/bin/env python

import logging

from googleads import ad_manager

from dfp.client import get_client

def get_line_items_for_order(order_id):
  """
  Gets all line items under an order with ID `order_id`.

  Args:
    order_id (number): the DFP ID of the order
  Returns:
    an array of line items
  """
  print('Getting line items for order ID {0}...'.format(order_id))
  client = get_client()
  line_item_service = client.GetService('LineItemService', version='v201908')
  statement = (ad_manager.StatementBuilder()
    .Where('OrderId = :order_id')
    .WithBindVariable('order_id', order_id))

  line_items = []
  while True:
    response = line_item_service.getLineItemsByStatement(
      statement.ToStatement())
    if 'results' in response and len(response['results']) > 0:
      line_items = line_items + response['results']
      statement.offset += statement.limit
    else:
      break

  print('Finished fetching line items.')

  return line_items

#!/usr/bin/env python

from unittest import TestCase
from mock import MagicMock, Mock, patch

import dfp.get_orders


@patch('googleads.ad_manager.AdManagerClient.LoadFromStorage')
class DFPServiceTests(TestCase):

  def test_get_all_orders(self, mock_dfp_client):
    """
    Ensure `get_all_orders` makes one call to DFP.
    """
    mock_dfp_client.return_value = MagicMock()

    # Response for fetching orders.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getOrdersByStatement) = MagicMock()

    dfp.get_orders.get_all_orders()

    # Confirm that it loaded the mock DFP client.
    mock_dfp_client.assert_called_once()

    expected_arg = {'query': ' LIMIT 500 OFFSET 0', 'values': None}
    (mock_dfp_client.return_value
      .GetService.return_value
      .getOrdersByStatement.assert_called_once_with(expected_arg)
      )

  def test_get_all_orders_unicode(self, mock_dfp_client):
    """
    Ensure `get_all_orders` prints when orders contain unicode characters.
    """
    mock_dfp_client.return_value = MagicMock()

    # Response for fetching orders.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getOrdersByStatement).side_effect = [
        {
          'totalResultSetSize': 1,
          'startIndex': 0,
          'results': [{
            'id': 152637489,
            'name': u'\xe4',
            'startDateTime': {},
            'endDateTime': {},
            'unlimitedEndDateTime': True,
            'status': 'DRAFT',
            'isArchived': False,
            'externalOrderId': 0,
            'currencyCode': 'USD',
            'advertiserId': 123456789,
            'creatorId': 123456789,
            'traffickerId': 123456789,
            'totalImpressionsDelivered': 0,
            'totalClicksDelivered': 0,
            'totalViewableImpressionsDelivered': 0,
            'totalBudget': {
              'currencyCode': 'USD',
              'microAmount': 0,
            },
            'lastModifiedByApp': 'tab-for-',
            'isProgrammatic': False,
            'lastModifiedDateTime': {},
          }]
        },
        {
          'totalResultSetSize': 0,
          'startIndex': 0,
        },
    ]

    dfp.get_orders.get_all_orders()

  def test_get_order_by_name(self, mock_dfp_client):
    """
    Ensure we make the correct call to DFP when getting an order
    by name.
    """
    mock_dfp_client.return_value = MagicMock()
    order_name = 'My Fake Order'

    # Response for fetching orders.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getOrdersByStatement) = MagicMock()

    dfp.get_orders.get_order_by_name(order_name)

    # Expected argument to use in call to DFP.
    expected_statement = {
      'query': 'WHERE name = :name LIMIT 500 OFFSET 0',
      'values': [{
        'value': {
          'value': order_name,
          'xsi_type': 'TextValue'
          },
          'key': 'name'
        }]
    }

    (mock_dfp_client.return_value
      .GetService.return_value
      .getOrdersByStatement.assert_called_once_with(expected_statement)
      )

  def test_get_order_by_name_return(self, mock_dfp_client):
    """
    Ensure we return the order when we get an order.
    """
    mock_dfp_client.return_value = MagicMock()
    order_name = 'My Fake Order'

    # Response for fetching orders.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getOrdersByStatement) = MagicMock(
        return_value={
          'totalResultSetSize': 1,
          'startIndex': 0,
          'results': [{
            'id': 152637489,
            'name': order_name,
            'startDateTime': {},
            'endDateTime': {},
            'unlimitedEndDateTime': True,
            'status': 'DRAFT',
            'isArchived': False,
            'externalOrderId': 0,
            'currencyCode': 'USD',
            'advertiserId': 123456789,
            'creatorId': 123456789,
            'traffickerId': 123456789,
            'totalImpressionsDelivered': 0,
            'totalClicksDelivered': 0,
            'totalViewableImpressionsDelivered': 0,
            'totalBudget': {
              'currencyCode': 'USD',
              'microAmount': 0,
            },
            'lastModifiedByApp': 'tab-for-',
            'isProgrammatic': False,
            'lastModifiedDateTime': {},
          }]
      }
    )

    order = dfp.get_orders.get_order_by_name(order_name)
    self.assertEqual(order['id'], 152637489)

  def test_get_no_order_by_name(self, mock_dfp_client):
    """
    Ensure we return None when an order does not exist.
    """
    mock_dfp_client.return_value = MagicMock()

    # Response for fetching orders.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getOrdersByStatement) = MagicMock(
        return_value={
          'totalResultSetSize': 0,
          'startIndex': 0,
      }
    )

    order = dfp.get_orders.get_order_by_name('A new order')
    self.assertIsNone(order)

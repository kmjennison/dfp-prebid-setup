
from unittest import TestCase
from mock import MagicMock, Mock, patch

import settings
import dfp.create_orders
from dfp.exceptions import BadSettingException, MissingSettingException


@patch('googleads.ad_manager.AdManagerClient.LoadFromStorage')
class DFPCreateOrderTests(TestCase):

  @patch('dfp.get_orders.get_order_by_name')
  def test_create_orders_call(self, mock_get_order_by_name, mock_dfp_client):
    """
    Ensure it calls DFP once with order info.
    """

    # Mock that no order exists with the same name.
    mock_get_order_by_name.return_value = None

    mock_dfp_client.return_value = MagicMock()

    (mock_dfp_client.return_value
      .GetService.return_value
      .createOrders) = MagicMock()

    order_name = 'My Fake Test Order'
    advertiser_id = 24681012
    trafficker_id = 12359113
    dfp.create_orders.create_order(order_name, advertiser_id, trafficker_id)

    expected_config = [
      dfp.create_orders.create_order_config(name=order_name,
        advertiser_id=advertiser_id, trafficker_id=trafficker_id)
    ]

    (mock_dfp_client.return_value
      .GetService.return_value
      .createOrders.assert_called_once_with(expected_config)
      )

  @patch.multiple('settings', DFP_USE_EXISTING_ORDER_IF_EXISTS=False)
  @patch('dfp.get_orders.get_order_by_name')
  def test_create_orders_duplicate_name_fail(self, mock_get_order_by_name, 
    mock_dfp_client):

    """
    Ensure it throws an Exception if an order with that name already exists
    and we should not modify the existing order.
    """

    # Mock that an order already exists with the same name.
    mock_get_order_by_name.return_value = {
      'id': 123456789,
      'name': 'My Test Order!'
    }

    order_name = 'My Test Order!'
    advertiser_id = 24681012
    trafficker_id = 12359113

    with self.assertRaises(BadSettingException):
      dfp.create_orders.create_order(order_name, advertiser_id, trafficker_id)

  @patch.multiple('settings', DFP_USE_EXISTING_ORDER_IF_EXISTS=True)
  @patch('dfp.get_orders.get_order_by_name')
  def test_create_orders_duplicate_name_success(self, mock_get_order_by_name, 
    mock_dfp_client):

    """
    Use an existing order with the same name if settings allow.
    """

    # Mock that an order already exists with the same name.
    mock_get_order_by_name.return_value = {
      'id': 123456789,
      'name': 'My Test Order!'
    }

    order_name = 'My Test Order!'
    advertiser_id = 24681012
    trafficker_id = 12359113

    order_id = dfp.create_orders.create_order(order_name, advertiser_id,
      trafficker_id)

    self.assertEqual(order_id, 123456789)

  @patch('dfp.get_orders.get_order_by_name')
  def test_return_order_id(self, mock_get_order_by_name, mock_dfp_client):
    """
    Ensure it returns the created order ID.
    """

    # Mock that no order exists with the same name.
    mock_get_order_by_name.return_value = None

    mock_dfp_client.return_value = MagicMock()

    order_name = 'Some Order!'
    advertiser_id = 97867564
    trafficker_id = 13243546

    # Mock DFP response.
    (mock_dfp_client.return_value
      .GetService.return_value
      .createOrders) = MagicMock(
        return_value=[{
          'id': 22233344,
          'name': order_name,
          'startDateTime': {},
          'endDateTime': {},
          'unlimitedEndDateTime': True,
          'status': 'DRAFT',
          'isArchived': False,
          'externalOrderId': 0,
          'currencyCode': 'USD',
          'advertiserId': advertiser_id,
          'creatorId': 123456789,
          'traffickerId': trafficker_id,
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
      )

    order_id = dfp.create_orders.create_order(order_name, advertiser_id,
      trafficker_id)

    self.assertEqual(order_id, 22233344)

  def test_order_config(self, mock_dfp_client):
    """
    Ensure order config creation is correct.
    """

    order_name = 'My Test Order!'
    advertiser_id = 24681012
    trafficker_id = 12359113

    config = dfp.create_orders.create_order_config(name=order_name,
        advertiser_id=advertiser_id, trafficker_id=trafficker_id)

    self.assertEqual(config, {
      'advertiserId': 24681012,
      'name': 'My Test Order!',
      'traffickerId': 12359113
      })

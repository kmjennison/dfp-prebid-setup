
from unittest import TestCase
from mock import MagicMock, Mock, patch

import settings
import dfp.create_orders
from dfp.exceptions import MissingSettingException

@patch.multiple('settings',
  DFP_ORDER_NAME='My Test Order!',
  DFP_ORDER_ADVERTISER_ID=24681012,
  DFP_ORDER_TRAFFICKER_ID=12359113)
@patch('googleads.dfp.DfpClient.LoadFromStorage')
class DFPServiceTests(TestCase):

  def test_create_orders_call(self, mock_dfp_client):
    """
    Ensure it calls DFP once with order info.
    """
    mock_dfp_client.return_value = MagicMock()

    (mock_dfp_client.return_value
      .GetService.return_value
      .createOrders) = MagicMock()

    order_name = 'My Test Order!'
    advertiser_id = 24681012
    trafficker_id = 12359113
    dfp.create_orders.main()

    expected_config = [
      dfp.create_orders.create_order_config(name=order_name,
        advertiser_id=advertiser_id, trafficker_id=trafficker_id)
    ]

    (mock_dfp_client.return_value
      .GetService.return_value
      .createOrders.assert_called_once_with(expected_config)
      )

  def test_create_orders_missing_name(self, mock_dfp_client):
    """
    Raises an exception when missing the name parameter.
    """
    mock_dfp_client.return_value = MagicMock()

    with patch('settings.DFP_ORDER_NAME', None):
      with self.assertRaises(MissingSettingException):
        dfp.create_orders.main()

  def test_create_orders_missing_advertiser_id(self, mock_dfp_client):
    """
    Raises an exception when missing the advertiser_id parameter.
    """
    mock_dfp_client.return_value = MagicMock()

    with patch('settings.DFP_ORDER_ADVERTISER_ID', None):
      with self.assertRaises(MissingSettingException):
        dfp.create_orders.main()

  def test_create_orders_missing_trafficker_id(self, mock_dfp_client):
    """
    Raises an exception when missing the trafficker_id parameter.
    """
    mock_dfp_client.return_value = MagicMock()

    with patch('settings.DFP_ORDER_TRAFFICKER_ID', None):
      with self.assertRaises(MissingSettingException):
        dfp.create_orders.main()

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


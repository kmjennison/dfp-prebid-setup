
from unittest import TestCase
from mock import MagicMock, Mock, patch

import dfp.service


class DFPServiceTests(TestCase):

  @patch('dfp.service.get_client')
  def test_get_all_orders(self, mock_dfp_client):
    """
    Ensure `get_all_orders` makes one call to DFP.
    """
    mock_dfp_client.return_value = MagicMock()

    # Response for fetching orders.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getOrdersByStatement) = MagicMock()

    dfp.service.get_all_orders()

    # Confirm that it loaded the mock DFP client.
    mock_dfp_client.assert_called_once()

    expected_arg = {'query': ' LIMIT 500 OFFSET 0', 'values': None}
    (mock_dfp_client.return_value
      .GetService.return_value
      .getOrdersByStatement.assert_called_once_with(expected_arg)
      )


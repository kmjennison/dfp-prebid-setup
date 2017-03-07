
import os
from unittest import TestCase
from mock import MagicMock, Mock, patch

import settings
import dfp.associate_line_items_and_creatives


@patch('googleads.dfp.DfpClient.LoadFromStorage')
class DFPCreateLICAsTests(TestCase):

  def test_association(self, mock_dfp_client):
    """
    Ensure it calls DFP with expected associations.
    """

    mock_dfp_client.return_value = MagicMock()
    dfp.associate_line_items_and_creatives.make_licas(
      [987654, 7654321, 5432109], [111222, 223344])

    expected_arg = [
      {
        'lineItemId': 987654,
        'creativeId': 111222
      },
      {
        'lineItemId': 987654,
        'creativeId': 223344
      },
      {
        'lineItemId': 7654321,
        'creativeId': 111222
      },
      {
        'lineItemId': 7654321,
        'creativeId': 223344
      },
      {
        'lineItemId': 5432109,
        'creativeId': 111222
      },
      {
        'lineItemId': 5432109,
        'creativeId': 223344
      },
    ]
    
    (mock_dfp_client.return_value
      .GetService.return_value
      .createLineItemCreativeAssociations.assert_called_once_with(expected_arg)
      )

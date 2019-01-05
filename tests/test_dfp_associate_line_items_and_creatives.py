
import os
from unittest import TestCase
from mock import MagicMock, Mock, patch

import settings
import dfp.associate_line_items_and_creatives


@patch('googleads.ad_manager.AdManagerClient.LoadFromStorage')
class DFPCreateLICAsTests(TestCase):

  def test_association(self, mock_dfp_client):
    """
    Ensure it calls DFP with expected associations.
    """

    mock_dfp_client.return_value = MagicMock()
    dfp.associate_line_items_and_creatives.make_licas(
      [987654, 7654321, 5432109], [111222, 223344])

    sizes = []

    expected_arg = [
      {
        'lineItemId': 987654,
        'creativeId': 111222,
        'sizes': sizes,
      },
      {
        'lineItemId': 987654,
        'creativeId': 223344,
        'sizes': sizes,
      },
      {
        'lineItemId': 7654321,
        'creativeId': 111222,
        'sizes': sizes,
      },
      {
        'lineItemId': 7654321,
        'creativeId': 223344,
        'sizes': sizes,
      },
      {
        'lineItemId': 5432109,
        'creativeId': 111222,
        'sizes': sizes,
      },
      {
        'lineItemId': 5432109,
        'creativeId': 223344,
        'sizes': sizes,
      },
    ]
    
    (mock_dfp_client.return_value
      .GetService.return_value
      .createLineItemCreativeAssociations.assert_called_once_with(expected_arg)
      )

  def test_association_with_size_overrides(self, mock_dfp_client):
    """
    Ensure it calls DFP with expected associations when overriding sizes.
    """

    mock_dfp_client.return_value = MagicMock()
    dfp.associate_line_items_and_creatives.make_licas(
      [987654, 7654321, 5432109], [111222, 223344],
      size_overrides=[
        {
          'width': '300',
          'height': '250'
        },
        {
          'width': '728',
          'height': '90'
        }
      ]
    )

    sizes = [
      {
        'width': '300',
        'height': '250'
      },
      {
        'width': '728',
        'height': '90'
      },
    ]

    expected_arg = [
      {
        'lineItemId': 987654,
        'creativeId': 111222,
        'sizes': sizes,
      },
      {
        'lineItemId': 987654,
        'creativeId': 223344,
        'sizes': sizes,
      },
      {
        'lineItemId': 7654321,
        'creativeId': 111222,
        'sizes': sizes,
      },
      {
        'lineItemId': 7654321,
        'creativeId': 223344,
        'sizes': sizes,
      },
      {
        'lineItemId': 5432109,
        'creativeId': 111222,
        'sizes': sizes,
      },
      {
        'lineItemId': 5432109,
        'creativeId': 223344,
        'sizes': sizes,
      },
    ]
    
    (mock_dfp_client.return_value
      .GetService.return_value
      .createLineItemCreativeAssociations.assert_called_once_with(expected_arg)
      )

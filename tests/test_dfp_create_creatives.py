
import os
from unittest import TestCase
from mock import MagicMock, Mock, patch

import settings
import dfp.create_creatives


@patch('googleads.ad_manager.AdManagerClient.LoadFromStorage')
class DFPCreateCreativesTests(TestCase):

  def test_create_creatives_items_call(self, mock_dfp_client):
    """
    Ensure it calls DFP once with creative info.
    """

    mock_dfp_client.return_value = MagicMock()

    creative_configs = [
      dfp.create_creatives.create_creative_config(
        name='My Creative',
        advertiser_id=1234567,
      )
    ]

    dfp.create_creatives.create_creatives(creative_configs)

    (mock_dfp_client.return_value
      .GetService.return_value
      .createCreatives.assert_called_once_with(creative_configs)
      )

  def test_create_creative_config(self, mock_dfp_client):
    """
    Ensure the line creative config is created as expected.
    """

    # Get expected snippet value.
    snippet_file_path = os.path.join(
      os.path.dirname(os.path.dirname(__file__)),
      'dfp', 'creative_snippet.html')
    with open(snippet_file_path, 'r') as snippet_file:
        snippet = snippet_file.read()

    self.assertEqual(
      dfp.create_creatives.create_creative_config(
        name='My Creative',
        advertiser_id=1234567,
      ),
      {
        'advertiserId': 1234567,
        'isSafeFrameCompatible': False,
        'name': 'My Creative',
        'size': {
          'height': '1',
          'width': '1'
        },
        'snippet': snippet,
        'xsi_type': 'ThirdPartyCreative'
       }
    )

  def test_create_creatives_returns_ids(self, mock_dfp_client):
    """
    Ensure it returns the IDs of created line items.
    """

    # Mock DFP response after creating line items.
    (mock_dfp_client.return_value
      .GetService.return_value
      .createCreatives) = MagicMock(return_value=[
        
        # Approximate shape of DFP creative response.
        {
          'advertiserId': 12345678,
          'id': 16273849,
          'name': 'My Nice Creative',
          'size': {
            'width': 1,
            'height': 1,
          },
          'isAspectRatio': False,
          'previewUrl': 'http://some-url.example',
          'lastModifiedDateTime': {},
          'snippet': '<script></script>',
          'expandedSnippet': '<script></script>',
          'sslScanResult': 'UNSCANNED',
          'sslManualOverride': 'NO_OVERRIDE',
          'lockedOrientation': 'FREE_ORIENTATION',
          'isSafeFrameCompatible': False,
        },

        # Some simple mock creatives.
        {
          'id': 444555666,
          'name': 'Another creative'
        },
        {
          'id': 999888777,
          'name': 'Blinking banner ad'
        },
      ])

    creative_configs = [{}, {}] # Mock does not matter.
    self.assertEqual(
      dfp.create_creatives.create_creatives(creative_configs),
      [16273849, 444555666, 999888777]
    )

  def test_build_creative_name(self, mock_dfp_client):
    """
    Ensure the creative name is formatted as expected.
    """

    self.assertEqual(
      dfp.create_creatives.build_creative_name('coolbiddr', 'Order Up!', 1),
      'coolbiddr: HB Order Up!, #1'
    )

    self.assertEqual(
      dfp.create_creatives.build_creative_name('coolbiddr', 'Order Up!', 2),
      'coolbiddr: HB Order Up!, #2'
    )

    self.assertEqual(
      dfp.create_creatives.build_creative_name('anotherpartner', 'ordrrr', 11),
      'anotherpartner: HB ordrrr, #11'
    )

  @patch('dfp.create_creatives.create_creative_config')
  def test_create_duplicate_creative_configs(self, mock_create_creative_config,
    mock_dfp_client):
    """
    Ensure we generate the correct array of creative configs.
    """

    # Mock the actual creative config.
    mock_create_creative_config.return_value = {'advertiserId': 12345}

    bidder_code = 'somebidder'
    order_name = 'An order'
    advertiser_id = 12345
    creative_num = 4

    configs = dfp.create_creatives.create_duplicate_creative_configs(
      bidder_code, order_name, advertiser_id, creative_num)

    # Assert we created the correct number of configs.
    self.assertEqual(mock_create_creative_config.call_count, creative_num)

    self.assertEqual(
      configs, 
      [
        {'advertiserId': 12345},
        {'advertiserId': 12345},
        {'advertiserId': 12345},
        {'advertiserId': 12345},
      ]
    )


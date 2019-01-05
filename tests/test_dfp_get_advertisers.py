
from unittest import TestCase

from googleads import ad_manager
from mock import MagicMock, Mock, patch

import settings
import dfp.get_advertisers
from dfp.exceptions import (
  BadSettingException,
  DFPObjectNotFound,
  MissingSettingException,
)


@patch('googleads.ad_manager.AdManagerClient.LoadFromStorage')
class DFPGetAdvertisersTests(TestCase):

  def test_get_advertiser_call(self, mock_dfp_client):
    """
    Ensure it calls DFP once with correct filter info.
    """
    mock_dfp_client.return_value = MagicMock()

    advertiser_name = 'Some Advertiser'

    # Mock DFP response.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getCompaniesByStatement) = MagicMock(
        return_value={
          'totalResultSetSize': 1,
          'startIndex': 0,
          'results': [{
            'id': 135792468,
            'name': advertiser_name,
            'type': 'AD_NETWORK',
            'creditStatus': 'ACTIVE',
            'lastModifiedDateTime': {} # some date
          }]
        }
      )

    dfp.get_advertisers.get_advertiser_id_by_name(advertiser_name)

    # Expected argument to use in call to DFP.
    expected_statement = {
      'query': 'WHERE name = :name LIMIT 500 OFFSET 0',
      'values': [{
        'value': {
          'value': advertiser_name,
          'xsi_type': 'TextValue'
          },
          'key': 'name'
        }]
    }

    (mock_dfp_client.return_value
      .GetService.return_value
      .getCompaniesByStatement.assert_called_once_with(expected_statement)
      )

  @patch.multiple('settings', DFP_CREATE_ADVERTISER_IF_DOES_NOT_EXIST=False)
  @patch('dfp.get_advertisers.create_advertiser')
  def test_get_no_advertiser(self, mock_create_advertiser, mock_dfp_client):
    """
    Ensure it raises an exception when the advertiser does not exist in DFP
    and the settings do not allow advertiser creation.
    """
    mock_dfp_client.return_value = MagicMock()

    advertiser_name = 'Boop, Inc.'

    # Mock DFP response.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getCompaniesByStatement) = MagicMock(
        return_value={
          'totalResultSetSize': 0,
          'startIndex': 0,
        }
      )

    with self.assertRaises(DFPObjectNotFound):
      dfp.get_advertisers.get_advertiser_id_by_name(advertiser_name)

    mock_create_advertiser.assert_not_called()

  @patch.multiple('settings', DFP_CREATE_ADVERTISER_IF_DOES_NOT_EXIST=True)
  @patch('dfp.get_advertisers.create_advertiser')
  def test_get_no_advertiser_create(self, mock_create_advertiser, 
    mock_dfp_client):
    """
    Ensure it calls to create an advertiser when one doesn't exist and 
    the settings allow for new advertiser creation.
    """
    mock_dfp_client.return_value = MagicMock()

    advertiser_name = 'Boop, Inc.'

    # Mock DFP response.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getCompaniesByStatement) = MagicMock(
        return_value={
          'totalResultSetSize': 0,
          'startIndex': 0,
        }
      )
    dfp.get_advertisers.get_advertiser_id_by_name(advertiser_name)
    mock_create_advertiser.assert_called_once_with(advertiser_name)

  def test_get_duplicate_advertisers(self, mock_dfp_client):
    """
    Ensure it raises an exception when multiple advertisers have the same
    name in DFP.
    """
    mock_dfp_client.return_value = MagicMock()

    advertiser_name = 'Not an Advertiser in DFP'

    # Mock DFP response.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getCompaniesByStatement) = MagicMock(
        return_value={
          'totalResultSetSize': 2,
          'startIndex': 0,
          'results': [
            {
              'id': 135792468,
              'name': advertiser_name,
              'type': 'AD_NETWORK',
              'creditStatus': 'ACTIVE',
              'lastModifiedDateTime': {} # some date
            },
            {
              'id': 246891357,
              'name': advertiser_name,
              'type': 'AD_NETWORK',
              'creditStatus': 'ACTIVE',
              'lastModifiedDateTime': {} # some date
            },
          ]
        }
      )

    with self.assertRaises(BadSettingException):
      dfp.get_advertisers.get_advertiser_id_by_name(advertiser_name)

  @patch.multiple('settings',
    DFP_ADVERTISER_NAME='Some Advertiser')
  @patch('dfp.get_advertisers.get_advertiser_id_by_name')
  def test_settings_advertiser_name(self, mock_get_advertiser,
    mock_dfp_client):
    """
    Ensures we use the advertiser name from the settings file.
    """
    mock_get_advertiser.return_value = 112234567
    advertiser_id = dfp.get_advertisers.main()
    mock_get_advertiser.assert_called_once_with('Some Advertiser')
    self.assertEqual(advertiser_id, 112234567)

  @patch.multiple('settings', DFP_ADVERTISER_NAME=None)
  def test_missing_advertiser_name_setting(self, mock_dfp_client):
    """
    Ensures we raise an exception if the advertiser name setting
    does not exist.
    """
    with self.assertRaises(MissingSettingException):
      dfp.get_advertisers.main()

  def test_create_advertiser_call(self, mock_dfp_client):
    """
    Ensure it calls DFP once with correct advertiser config.
    """
    mock_dfp_client.return_value = MagicMock()

    advertiser_name = 'A New Advertiser'
    dfp.get_advertisers.create_advertiser(advertiser_name)
    expected_config = [
      {
        'name': advertiser_name,
        'type': 'AD_NETWORK'
      }
    ]

    (mock_dfp_client.return_value
      .GetService.return_value
      .createCompanies.assert_called_once_with(expected_config)
      )

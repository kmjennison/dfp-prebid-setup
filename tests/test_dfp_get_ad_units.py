
from unittest import TestCase
from mock import MagicMock, Mock, patch

import dfp.get_ad_units
from dfp.exceptions import (
  BadSettingException,
  DFPObjectNotFound,
  MissingSettingException
)


@patch('googleads.ad_manager.AdManagerClient.LoadFromStorage')
class DFPGetAdUnitsTests(TestCase):

  def test_get_placement_by_name_call(self, mock_dfp_client):
    """
    Ensure we make the correct call to DFP when getting a an ad unit
    by name.
    """
    mock_dfp_client.return_value = MagicMock()
    ad_unit_name = 'My_Nice_Ad_Unit'

    # Response from DFP.
    (mock_dfp_client.return_value
     .GetService.return_value
     .getAdUnitsByStatement) = MagicMock(
      return_value={
        'totalResultSetSize': 1,
        'startIndex': 0,
        'results': [{
          'id': '11122233344',
          'parentId': '12345678',
          'hasChildren': False,
          'parentPath': [
            {
              'id': '12345678',
              'name': 'ca-pub-0000000000000000',
              'adUnitCode': 'ca-pub-0000000000000000'
            }
          ],
          'name': 'My_Nice_Ad_Unit',
          'description': None,
          'targetWindow': 'BLANK',
          'status': 'ACTIVE',
          'adUnitCode': 'My_Nice_Ad_Unit',
          'adUnitSizes': [
            {
              'size': {
                'width': 300,
                'height': 250,
                'isAspectRatio': False
              },
              'environmentType': 'BROWSER',
              'companions': [],
              'fullDisplayString': '300x250'
            }
          ],
          'isInterstitial': False,
          'isNative': False,
          'isFluid': False,
          'explicitlyTargeted': False,
          'adSenseSettings': {
            'adSenseEnabled': False,
            'borderColor': 'FFFFFF',
            'titleColor': '0000FF',
            'backgroundColor': 'FFFFFF',
            'textColor': '000000',
            'urlColor': '008000',
            'adType': 'TEXT_AND_IMAGE',
            'borderStyle': 'DEFAULT',
            'fontFamily': 'DEFAULT',
            'fontSize': 'DEFAULT'
          },
          'adSenseSettingsSource': 'PARENT',
          'appliedLabelFrequencyCaps': [],
          'effectiveLabelFrequencyCaps': [],
          'appliedLabels': [],
          'effectiveAppliedLabels': [],
          'effectiveTeamIds': [],
          'appliedTeamIds': [],
          'lastModifiedDateTime': {},
          'smartSizeMode': 'NONE',
          'refreshRate': None,
          'externalSetTopBoxChannelId': None,
          'isSetTopBoxEnabled': False
        }]
      }
    )

    dfp.get_ad_units.get_ad_unit_by_name(ad_unit_name)

    # Expected argument to use in call to DFP.
    expected_statement = {
      'query': 'WHERE name = :name LIMIT 500 OFFSET 0',
      'values': [{
        'key': 'name',
        'value': {
          'value': ad_unit_name,
          'xsi_type': 'TextValue'
          },
        }]
    }

    (mock_dfp_client.return_value
      .GetService.return_value
      .getAdUnitsByStatement.assert_called_once_with(expected_statement)
      )

  def test_get_placement_by_name(self, mock_dfp_client):
    """
    Ensure we return the ad unit when it's fetched successfully.
    """
    mock_dfp_client.return_value = MagicMock()
    ad_unit_name = 'My_Neat_Ad_Unit'

    # Response from DFP.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getAdUnitsByStatement) = MagicMock(
      return_value={
        'totalResultSetSize': 1,
        'startIndex': 0,
        'results': [{
          'id': '11122233344',
          'parentId': '12345678',
          'hasChildren': False,
          'parentPath': [
            {
              'id': '12345678',
              'name': 'ca-pub-0000000000000000',
              'adUnitCode': 'ca-pub-0000000000000000'
            }
          ],
          'name': 'My_Neat_Ad_Unit',
          'description': None,
          'targetWindow': 'BLANK',
          'status': 'ACTIVE',
          'adUnitCode': 'My_Neat_Ad_Unit',
          'adUnitSizes': [
            {
              'size': {
                'width': 300,
                'height': 250,
                'isAspectRatio': False
              },
              'environmentType': 'BROWSER',
              'companions': [],
              'fullDisplayString': '300x250'
            }
          ],
          'isInterstitial': False,
          'isNative': False,
          'isFluid': False,
          'explicitlyTargeted': False,
          'adSenseSettings': {
            'adSenseEnabled': False,
            'borderColor': 'FFFFFF',
            'titleColor': '0000FF',
            'backgroundColor': 'FFFFFF',
            'textColor': '000000',
            'urlColor': '008000',
            'adType': 'TEXT_AND_IMAGE',
            'borderStyle': 'DEFAULT',
            'fontFamily': 'DEFAULT',
            'fontSize': 'DEFAULT'
          },
          'adSenseSettingsSource': 'PARENT',
          'appliedLabelFrequencyCaps': [],
          'effectiveLabelFrequencyCaps': [],
          'appliedLabels': [],
          'effectiveAppliedLabels': [],
          'effectiveTeamIds': [],
          'appliedTeamIds': [],
          'lastModifiedDateTime': {},
          'smartSizeMode': 'NONE',
          'refreshRate': None,
          'externalSetTopBoxChannelId': None,
          'isSetTopBoxEnabled': False
        }]
      }
    )

    placement = dfp.get_ad_units.get_ad_unit_by_name(ad_unit_name)
    self.assertEqual(placement['id'], '11122233344')

  def test_get_no_ad_unit_by_name(self, mock_dfp_client):
    """
    Ensure we throw an exception when the placement doesn't exist.
    """
    mock_dfp_client.return_value = MagicMock()

    # Response from DFP.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getAdUnitsByStatement) = MagicMock(
        return_value={
          'totalResultSetSize': 0,
          'startIndex': 0,
      }
    )

    with self.assertRaises(DFPObjectNotFound):
      ad_unit = dfp.get_ad_units.get_ad_unit_by_name(
        'Not_an_Existing_Ad_Unit')

  @patch('dfp.get_ad_units.get_ad_unit_by_name')
  def test_get_ad_unit_ids_by_name(self, mock_get_ad_unit_id_by_name,
    mock_dfp_client):
    """
    Ensures we return ad unit IDs.
    """

    # Fake returned ad unit. Return a different one each time
    # it is called.
    mock_get_ad_unit_id_by_name.side_effect = [
      {
        'id': '11122233344',
        'parentId': '12345678',
        'hasChildren': False,
        'parentPath': [
          {
            'id': '12345678',
            'name': 'ca-pub-0000000000000000',
            'adUnitCode': 'ca-pub-0000000000000000'
          }
        ],
        'name': 'Ad_Unit_One',
        'description': None,
        'targetWindow': 'BLANK',
        'status': 'ACTIVE',
        'adUnitCode': 'Ad_Unit_One',
        'adUnitSizes': [
          {
            'size': {
              'width': 300,
              'height': 250,
              'isAspectRatio': False
            },
            'environmentType': 'BROWSER',
            'companions': [],
            'fullDisplayString': '300x250'
          }
        ],
        'isInterstitial': False,
        'isNative': False,
        'isFluid': False,
        'explicitlyTargeted': False,
        'adSenseSettings': {
          'adSenseEnabled': False,
          'borderColor': 'FFFFFF',
          'titleColor': '0000FF',
          'backgroundColor': 'FFFFFF',
          'textColor': '000000',
          'urlColor': '008000',
          'adType': 'TEXT_AND_IMAGE',
          'borderStyle': 'DEFAULT',
          'fontFamily': 'DEFAULT',
          'fontSize': 'DEFAULT'
        },
        'adSenseSettingsSource': 'PARENT',
        'appliedLabelFrequencyCaps': [],
        'effectiveLabelFrequencyCaps': [],
        'appliedLabels': [],
        'effectiveAppliedLabels': [],
        'effectiveTeamIds': [],
        'appliedTeamIds': [],
        'lastModifiedDateTime': {},
        'smartSizeMode': 'NONE',
        'refreshRate': None,
        'externalSetTopBoxChannelId': None,
        'isSetTopBoxEnabled': False
      },
      {
        'id': '22233344455',
        'parentId': '12345678',
        'hasChildren': False,
        'parentPath': [
          {
            'id': '12345678',
            'name': 'ca-pub-0000000000000000',
            'adUnitCode': 'ca-pub-0000000000000000'
          }
        ],
        'name': 'Ad_Unit_Two',
        'description': None,
        'targetWindow': 'BLANK',
        'status': 'ACTIVE',
        'adUnitCode': 'Ad_Unit_Two',
        'adUnitSizes': [
          {
            'size': {
              'width': 300,
              'height': 250,
              'isAspectRatio': False
            },
            'environmentType': 'BROWSER',
            'companions': [],
            'fullDisplayString': '300x250'
          }
        ],
        'isInterstitial': False,
        'isNative': False,
        'isFluid': False,
        'explicitlyTargeted': False,
        'adSenseSettings': {
          'adSenseEnabled': False,
          'borderColor': 'FFFFFF',
          'titleColor': '0000FF',
          'backgroundColor': 'FFFFFF',
          'textColor': '000000',
          'urlColor': '008000',
          'adType': 'TEXT_AND_IMAGE',
          'borderStyle': 'DEFAULT',
          'fontFamily': 'DEFAULT',
          'fontSize': 'DEFAULT'
        },
        'adSenseSettingsSource': 'PARENT',
        'appliedLabelFrequencyCaps': [],
        'effectiveLabelFrequencyCaps': [],
        'appliedLabels': [],
        'effectiveAppliedLabels': [],
        'effectiveTeamIds': [],
        'appliedTeamIds': [],
        'lastModifiedDateTime': {},
        'smartSizeMode': 'NONE',
        'refreshRate': None,
        'externalSetTopBoxChannelId': None,
        'isSetTopBoxEnabled': False
      }
    ]
    ad_unit_ids = dfp.get_ad_units.get_ad_unit_ids_by_name(
      ['Ad_Unit_One', 'Ad_Unit_Two'])
    self.assertEqual(ad_unit_ids, ['11122233344', '22233344455'])

  @patch.multiple('settings',
    DFP_TARGETED_AD_UNIT_NAMES=['My_Ad_Unit', 'Another_Ad_Unit'])
  @patch('dfp.get_ad_units.get_ad_unit_ids_by_name')
  def test_settings_placements(self, get_ad_unit_ids_by_name,
    mock_dfp_client):
    """
    Ensures we use the ad unit names from the settings file.
    """
    
    # Fake returned placement IDs
    get_ad_unit_ids_by_name.return_value = ['23344556', '123456789']
    dfp.get_ad_units.main()
    get_ad_unit_ids_by_name.assert_called_once_with(
      ['My_Ad_Unit', 'Another_Ad_Unit'])

  @patch.multiple('settings', DFP_TARGETED_AD_UNIT_NAMES=None)
  def test_create_orders_missing_ad_units_setting(self, mock_dfp_client):
    """
    Ensures we raise an exception if the ad unit setting
    does not exist.
    """
    
    with self.assertRaises(MissingSettingException):
      dfp.get_ad_units.main()

  @patch.multiple('settings', DFP_TARGETED_AD_UNIT_NAMES=[])
  def test_create_orders_bad_ad_units_setting(self, mock_dfp_client):
    """
    Ensures we raise an exception if the ad units setting
    does not contain any ad unit names.
    """
    
    with self.assertRaises(BadSettingException):
      dfp.get_ad_units.main()

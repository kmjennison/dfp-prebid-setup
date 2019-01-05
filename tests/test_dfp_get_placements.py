
from unittest import TestCase
from mock import MagicMock, Mock, patch

import dfp.get_placements
from dfp.exceptions import (
  BadSettingException,
  DFPObjectNotFound,
  MissingSettingException
)


@patch('googleads.ad_manager.AdManagerClient.LoadFromStorage')
class DFPGetPlacementsTests(TestCase):

  def test_get_placement_by_name_call(self, mock_dfp_client):
    """
    Ensure we make the correct call to DFP when getting a a placement
    by name.
    """
    mock_dfp_client.return_value = MagicMock()
    placement_name = 'My Nice Placement'

    # Response from DFP.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getPlacementsByStatement) = MagicMock(
        return_value={
          'totalResultSetSize': 1,
          'startIndex': 0,
          'results': [{
            'targetingDescription': None,
            'targetingSiteName': None,
            'targetingAdLocation': None,
            'id': 22334455,
            'name': placement_name,
            'description': None,
            'placementCode': "111222333444555666",
            'status': "ACTIVE",
            'isAdSenseTargetingEnabled': False,
            'adSenseTargetingLocale': "und",
            'targetedAdUnitIds': ['123456789'],
            'lastModifiedDateTime': {},
          }]
        }
    )

    dfp.get_placements.get_placement_by_name(placement_name)

    # Expected argument to use in call to DFP.
    expected_statement = {
      'query': 'WHERE name = :name LIMIT 500 OFFSET 0',
      'values': [{
        'value': {
          'value': placement_name,
          'xsi_type': 'TextValue'
          },
          'key': 'name'
        }]
    }

    (mock_dfp_client.return_value
      .GetService.return_value
      .getPlacementsByStatement.assert_called_once_with(expected_statement)
      )

  def test_get_placement_by_name(self, mock_dfp_client):
    """
    Ensure we return the placement when it's fetched successfully.
    """
    mock_dfp_client.return_value = MagicMock()
    placement_name = 'My Neat Placement'

    # Response from DFP.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getPlacementsByStatement) = MagicMock(
        return_value={
          'totalResultSetSize': 1,
          'startIndex': 0,
          'results': [{
            'targetingDescription': None,
            'targetingSiteName': None,
            'targetingAdLocation': None,
            'id': 22334455,
            'name': placement_name,
            'description': None,
            'placementCode': "111222333444555666",
            'status': "ACTIVE",
            'isAdSenseTargetingEnabled': False,
            'adSenseTargetingLocale': "und",
            'targetedAdUnitIds': ['123456789'],
            'lastModifiedDateTime': {},
          }]
        }
    )

    placement = dfp.get_placements.get_placement_by_name(placement_name)
    self.assertEqual(placement['id'], 22334455)

  def test_get_no_placement_by_name(self, mock_dfp_client):
    """
    Ensure we throw an exception when the placement doesn't exist.
    """
    mock_dfp_client.return_value = MagicMock()

    # Response from DFP.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getPlacementsByStatement) = MagicMock(
        return_value={
          'totalResultSetSize': 0,
          'startIndex': 0,
      }
    )

    with self.assertRaises(DFPObjectNotFound):
      placement = dfp.get_placements.get_placement_by_name(
        'Not an Existing Placement')

  @patch('dfp.get_placements.get_placement_by_name')
  def test_get_placement_ids_by_name(self, mock_get_placement_by_name, 
    mock_dfp_client):
    """
    Ensures we return placement IDs.
    """

    # Fake returned placement. Return a different one each time
    # it is called.
    mock_get_placement_by_name.side_effect = [
      {
        'targetingDescription': None,
        'targetingSiteName': None,
        'targetingAdLocation': None,
        'id': 9988776655,
        'name': 'Placement One.',
        'description': None,
        'placementCode': "111222333444555666",
        'status': "ACTIVE",
        'isAdSenseTargetingEnabled': False,
        'adSenseTargetingLocale': "und",
        'targetedAdUnitIds': ['123456789'],
        'lastModifiedDateTime': {},
      },
      {
        'targetingDescription': None,
        'targetingSiteName': None,
        'targetingAdLocation': None,
        'id': 13571357,
        'name': 'Placement Two.',
        'description': None,
        'placementCode': "111222333444555666",
        'status': "ACTIVE",
        'isAdSenseTargetingEnabled': False,
        'adSenseTargetingLocale': "und",
        'targetedAdUnitIds': ['123456789'],
        'lastModifiedDateTime': {},
      }
    ]
    placement_ids = dfp.get_placements.get_placement_ids_by_name(
      ['Placement One.', 'Placement Two.'])
    self.assertEqual(placement_ids, [9988776655, 13571357])

  @patch.multiple('settings',
    DFP_TARGETED_PLACEMENT_NAMES=['My Placement!', 'Another placment'])
  @patch('dfp.get_placements.get_placement_ids_by_name')
  def test_settings_placements(self, mock_get_placement_ids_by_names,
    mock_dfp_client):
    """
    Ensures we use the placement names from the settings file.
    """
    
    # Fake returned placement IDs
    mock_get_placement_ids_by_names.return_value = [223344556, 123456789]
    dfp.get_placements.main()
    mock_get_placement_ids_by_names.assert_called_once_with(
      ['My Placement!', 'Another placment'])

  @patch.multiple('settings', DFP_TARGETED_PLACEMENT_NAMES=None)
  def test_create_orders_missing_placements_setting(self, mock_dfp_client):
    """
    Ensures we raise an exception if the placements setting
    does not exist.
    """
    
    with self.assertRaises(MissingSettingException):
      dfp.get_placements.main()

  @patch.multiple('settings', DFP_TARGETED_PLACEMENT_NAMES=[])
  def test_create_orders_bad_placements_setting(self, mock_dfp_client):
    """
    Ensures we raise an exception if the placements setting
    does not contain any placement names.
    """
    
    with self.assertRaises(BadSettingException):
      dfp.get_placements.main()

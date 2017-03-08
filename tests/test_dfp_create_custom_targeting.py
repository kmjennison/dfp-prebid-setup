
from unittest import TestCase
from mock import MagicMock, Mock, patch

import dfp.create_custom_targeting


@patch('googleads.dfp.DfpClient.LoadFromStorage')
class DFPCreateCustomTargetingTests(TestCase):

  def test_create_targeting_key(self, mock_dfp_client):
    """
    Ensure it calls DFP to create a key and returns the key ID.
    """
    mock_dfp_client.return_value = MagicMock()

    display_name = 'My Key'
    name = 'my-key'

    # Mock response from DFP.
    (mock_dfp_client.return_value
      .GetService.return_value
      .createCustomTargetingKeys) = MagicMock(return_value=[
        {
          'customTargetingKeyId': 987654,
          'displayName': 'My Key',
          'id': 1324354657,
          'name': 'my-key'
        },
      ])

    response = dfp.create_custom_targeting.create_targeting_key(name, 
      display_name)

    expected_arg = [
      {
        'displayName': display_name,
        'name': name,
        'type': 'FREEFORM'
      }
    ]

    (mock_dfp_client.return_value
      .GetService.return_value
      .createCustomTargetingKeys.assert_called_once_with(expected_arg)
      )

    self.assertEqual(response, 1324354657)

  def test_create_targeting_value(self, mock_dfp_client):
    """
    Ensure it calls DFP to create values.
    """
    mock_dfp_client.return_value = MagicMock()

    key_id = 2468
    values = ['a-value', 'another-value', 'yet-another']

    response = dfp.create_custom_targeting.create_targeting_values(values, 
      key_id)

    expected_arg = [
      {
        'customTargetingKeyId': key_id,
        'displayName': 'a-value',
        'name': 'a-value',
        'matchType': 'EXACT'
      },
      {
        'customTargetingKeyId': key_id,
        'displayName': 'another-value',
        'name': 'another-value',
        'matchType': 'EXACT'
      },
      {
        'customTargetingKeyId': key_id,
        'displayName': 'yet-another',
        'name': 'yet-another',
        'matchType': 'EXACT'
      },
    ]
    
    (mock_dfp_client.return_value
      .GetService.return_value
      .createCustomTargetingValues.assert_called_once_with(expected_arg)
      )
    
    self.assertIsNone(response)


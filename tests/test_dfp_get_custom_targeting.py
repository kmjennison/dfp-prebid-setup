
from unittest import TestCase
from mock import MagicMock, Mock, patch

import dfp.get_custom_targeting


@patch('googleads.dfp.DfpClient.LoadFromStorage')
class DFPServiceTests(TestCase):

  def test_get_targeting_by_key_name_call_no_key(self, mock_dfp_client):
    """
    Ensure it makes one call to DFP to get the key info.
    """
    mock_dfp_client.return_value = MagicMock()

    # Mock response from DFP.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getCustomTargetingKeysByStatement) = MagicMock()

    response = dfp.get_custom_targeting.get_targeting_by_key_name('some-key')

    (mock_dfp_client.return_value
      .GetService.return_value
      .getCustomTargetingKeysByStatement.assert_called_once()
      )

    # It should not fetch values because the key does not exist.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getCustomTargetingValuesByStatement.assert_not_called()
      )

    self.assertIsNone(response)

  def test_get_targeting_by_key_name_call_key_exists(self, mock_dfp_client):
    """
    Ensure it makes a call to DFP to get the key info and calls to get the
    values.
    """
    mock_dfp_client.return_value = MagicMock()

    # Mock response from DFP for key fetching.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getCustomTargetingKeysByStatement) = MagicMock(
        return_value={
          'totalResultSetSize': 1,
          'startIndex': 0,
          'results': [{
            'id': 987654,
            'name': 'hb_pb',
            'displayName': 'hb_pb',
            'type': 'FREEFORM',
            'status': 'ACTIVE',
          }]
      })

    # Mock response from DFP for values fetching.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getCustomTargetingValuesByStatement) = MagicMock(
        return_value={
          'totalResultSetSize': 1,
          'startIndex': 0,
          'results': [
            {
              'customTargetingKeyId': 987654,
              'id': 1324354657,
              'name': '12.50',
              'displayName': '12.50',
              'matchType': 'EXACT',
              'status': 'ACTIVE',
            },
            {
              'customTargetingKeyId': 987654,
              'id': 3546576879,
              'name': '20.00',
              'displayName': '20.00',
              'matchType': 'EXACT',
              'status': 'ACTIVE',
            }
          ]
      })

    response = dfp.get_custom_targeting.get_targeting_by_key_name('hb_pb')

    (mock_dfp_client.return_value
      .GetService.return_value
      .getCustomTargetingKeysByStatement.assert_called_once()
      )

    # It should not fetch values because the key does not exist.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getCustomTargetingValuesByStatement.assert_called_once()
      )

    self.assertEqual(response,
      [
        {
          'customTargetingKeyId': 987654,
          'displayName': '12.50',
          'id': 1324354657,
          'name': '12.50'
        },
        {
          'customTargetingKeyId': 987654,
          'displayName': '20.00',
          'id': 3546576879,
          'name': '20.00'
        }
      ]
    )

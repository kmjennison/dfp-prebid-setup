
from unittest import TestCase

from googleads import ad_manager
from mock import MagicMock, Mock, patch

import settings
import dfp.get_users
from dfp.exceptions import DFPObjectNotFound, MissingSettingException


@patch('googleads.ad_manager.AdManagerClient.LoadFromStorage')
class DFPGetUsersTests(TestCase):

  def test_get_user_call(self, mock_dfp_client):
    """
    Ensure it calls DFP once with correct user filter info.
    """
    mock_dfp_client.return_value = MagicMock()

    test_email = 'fakeemail@gmail.com'

    # Mock DFP response for user fetch.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getUsersByStatement) = MagicMock(
        return_value={
          'totalResultSetSize': 1,
          'startIndex': 0,
          'results': [{
            'id': 135792468,
            'name': 'Fake Person',
            'email': test_email,
            'roleId': -1,
            'roleName': 'Administrator',
            'isActive': True,
            'isEmailNotificationAllowed': False,
            'isServiceAccount': False,
          }]
        }
      )

    dfp.get_users.get_user_id_by_email(test_email)

    # Expected argument to use in call to DFP.
    expected_statement = {
      'query': 'WHERE email = :email LIMIT 500 OFFSET 0',
      'values': [{
        'value': {
          'value': 'fakeemail@gmail.com',
          'xsi_type': 'TextValue'
          },
          'key': 'email'
        }]
    }

    (mock_dfp_client.return_value
      .GetService.return_value
      .getUsersByStatement.assert_called_once_with(expected_statement)
      )

  def test_get_user_call_no_user(self, mock_dfp_client):
    """
    Ensure it raises an exception when the user does not exist
    in DFP.
    """
    mock_dfp_client.return_value = MagicMock()

    test_email = 'not_a_dfp_user@gmail.com'

    # Mock DFP response for user fetch.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getUsersByStatement) = MagicMock(
        return_value={
          'totalResultSetSize': 0,
          'startIndex': 0,
        }
      )

    with self.assertRaises(DFPObjectNotFound):
      dfp.get_users.get_user_id_by_email(test_email)

  def test_user_id_returned(self, mock_dfp_client):
    """
    Ensure it returns the correct DFP user ID.
    """
    mock_dfp_client.return_value = MagicMock()

    test_email = 'fakeemail@gmail.com'

    # Mock DFP response for user fetch.
    (mock_dfp_client.return_value
      .GetService.return_value
      .getUsersByStatement) = MagicMock(
        return_value={
          'totalResultSetSize': 1,
          'startIndex': 0,
          'results': [{
            'id': 135792468,
            'name': 'Fake Person',
            'email': test_email,
            'roleId': -1,
            'roleName': 'Administrator',
            'isActive': True,
            'isEmailNotificationAllowed': False,
            'isServiceAccount': False,
          }]
        }
      )

    user_id = dfp.get_users.get_user_id_by_email(test_email)

    self.assertEqual(user_id, 135792468)

  @patch.multiple('settings',
    DFP_USER_EMAIL_ADDRESS='email_in_settings@example.com')
  @patch('dfp.get_users.get_user_id_by_email')
  def test_settings_user_email(self, mock_get_user_by_email, mock_dfp_client):
    """
    Ensures we use the email from the settings file.
    """
    mock_get_user_by_email.return_value = 223344556 # Fake returned user ID
    user_id = dfp.get_users.main()
    mock_get_user_by_email.assert_called_once_with(
      'email_in_settings@example.com')
    self.assertEqual(user_id, 223344556)

  @patch.multiple('settings', DFP_USER_EMAIL_ADDRESS=None)
  def test_create_orders_missing_email(self, mock_dfp_client):
    """
    Ensures we raise an exception if the user email setting
    does not exist.
    """
    
    with self.assertRaises(MissingSettingException):
      dfp.get_users.main()

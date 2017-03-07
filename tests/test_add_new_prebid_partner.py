
from unittest import TestCase

from mock import patch

import settings
from dfp.exceptions import BadSettingException, MissingSettingException
import tasks.add_new_prebid_partner

email = 'fakeuser@example.com'
advertiser = 'My Advertiser'
order = 'My Cool Order'
placements = ['id-1', 'id-42']
bidder_code = 'mypartner'
price_buckets = {
  'precision': 2,
  'min' : 0,
  'max' : 20,
  'increment': 0.10,
}

@patch.multiple('settings',
  DFP_USER_EMAIL_ADDRESS=email,
  DFP_ADVERTISER_NAME=advertiser,
  DFP_ORDER_NAME=order,
  DFP_TARGETED_PLACEMENT_NAMES=placements,
  PREBID_BIDDER_CODE=bidder_code,
  PREBID_PRICE_BUCKETS=price_buckets,
  DFP_CREATE_ADVERTISER_IF_DOES_NOT_EXIST=False)
class AddNewPrebidPartnerTests(TestCase):

  def test_missing_email_setting(self):
    """
    It throws an exception with a missing setting.
    """
    settings.DFP_USER_EMAIL_ADDRESS = None
    with self.assertRaises(MissingSettingException):
      tasks.add_new_prebid_partner.main()

  def test_missing_advertiser_setting(self):
    """
    It throws an exception with a missing setting.
    """
    settings.DFP_ADVERTISER_NAME = None
    with self.assertRaises(MissingSettingException):
      tasks.add_new_prebid_partner.main()

  def test_missing_order_setting(self):
    """
    It throws an exception with a missing setting.
    """
    settings.DFP_ORDER_NAME = None
    with self.assertRaises(MissingSettingException):
      tasks.add_new_prebid_partner.main()


  def test_missing_placement_setting(self):
    """
    It throws an exception with a missing setting.
    """
    settings.DFP_TARGETED_PLACEMENT_NAMES = None
    with self.assertRaises(MissingSettingException):
      tasks.add_new_prebid_partner.main()


  def test_missing_bidder_code_setting(self):
    """
    It throws an exception with a missing setting.
    """
    settings.PREBID_BIDDER_CODE = None
    with self.assertRaises(MissingSettingException):
      tasks.add_new_prebid_partner.main()

  def test_price_bucket_validity_missing_key(self):
    """
    It throws an exception of the price bucket setting
    is missing keys.
    """
    settings.PREBID_PRICE_BUCKETS={
      'precision': 2,
      'min' : 0,
      # 'max' : 20, # missing this key
      'increment': 0.10,
    }
    with self.assertRaises(BadSettingException):
      tasks.add_new_prebid_partner.main()

  def test_price_bucket_validity_bad_values(self):
    """
    It throws an exception of the price bucket setting
    has bad value types.
    """
    settings.PREBID_PRICE_BUCKETS={
      'precision': 2,
      'min' : '$0', # bad value type
      'max' : 20,
      'increment': 0.10,
    }
    with self.assertRaises(BadSettingException):
      tasks.add_new_prebid_partner.main()

  def test_price_bucket_validity_bad_values_again(self):
    """
    It throws an exception of the price bucket setting
    has bad value types.
    """
    settings.PREBID_PRICE_BUCKETS={
      'precision': 2,
      'min' : 0,
      'max' : 20,
      'increment': {'inc': 0.10}, # bad value type
    }
    with self.assertRaises(BadSettingException):
      tasks.add_new_prebid_partner.main()

  @patch('tasks.add_new_prebid_partner.setup_partner')
  @patch('tasks.add_new_prebid_partner.raw_input', return_value='n')
  def test_user_confirmation_rejected(self, mock_raw_input, 
    mock_setup_partners):
    """
    Make sure we exit when the user rejects the confirmation.
    """
    tasks.add_new_prebid_partner.main()
    mock_setup_partners.assert_not_called()

  @patch('tasks.add_new_prebid_partner.setup_partner')
  @patch('tasks.add_new_prebid_partner.raw_input', return_value='asdf')
  def test_user_confirmation_not_accepted(self, mock_raw_input, 
    mock_setup_partners):
    """
    Make sure we exit when the user types something other than 'y'.
    """
    tasks.add_new_prebid_partner.main()
    mock_setup_partners.assert_not_called()

  @patch('tasks.add_new_prebid_partner.setup_partner')
  @patch('tasks.add_new_prebid_partner.raw_input', return_value='y')
  def test_user_confirmation_accepted(self, mock_raw_input, 
    mock_setup_partners):
    """
    Make sure we start the process when the user confirms we should proceed.
    """
    tasks.add_new_prebid_partner.main()
    mock_setup_partners.assert_called_once_with(email, advertiser, order,
      placements, bidder_code, price_buckets)

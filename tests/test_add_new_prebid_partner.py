
from unittest import TestCase

from mock import MagicMock, patch

import settings
import tasks.add_new_prebid_partner
from dfp.exceptions import BadSettingException, MissingSettingException
from tasks.add_new_prebid_partner import DFPValueIdGetter
from tasks.price_utils import (
  get_prices_array,
)

email = 'fakeuser@example.com'
advertiser = 'My Advertiser'
order = 'My Cool Order'
placements = ['My Site Leaderboard', 'Another Placement']
ad_units = ['Leaderboard Ad Unit', 'Another Ad Unit']
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
bidder_code = 'mypartner'
price_buckets = {
  'precision': 2,
  'min' : 0,
  'max' : 20,
  'increment': 0.10,
}
prices = get_prices_array(price_buckets)

@patch.multiple('settings',
  DFP_USER_EMAIL_ADDRESS=email,
  DFP_ADVERTISER_NAME=advertiser,
  DFP_ORDER_NAME=order,
  DFP_TARGETED_PLACEMENT_NAMES=placements,
  DFP_TARGETED_AD_UNIT_NAMES=ad_units,
  DFP_PLACEMENT_SIZES = sizes,
  PREBID_BIDDER_CODE=bidder_code,
  PREBID_PRICE_BUCKETS=price_buckets,
  DFP_CREATE_ADVERTISER_IF_DOES_NOT_EXIST=False)
@patch('googleads.ad_manager.AdManagerClient.LoadFromStorage')
class AddNewPrebidPartnerTests(TestCase):

  def test_missing_email_setting(self, mock_dfp_client):
    """
    It throws an exception with a missing setting.
    """
    settings.DFP_USER_EMAIL_ADDRESS = None
    with self.assertRaises(MissingSettingException):
      tasks.add_new_prebid_partner.main()

  def test_missing_advertiser_setting(self, mock_dfp_client):
    """
    It throws an exception with a missing setting.
    """
    settings.DFP_ADVERTISER_NAME = None
    with self.assertRaises(MissingSettingException):
      tasks.add_new_prebid_partner.main()

  def test_missing_order_setting(self, mock_dfp_client):
    """
    It throws an exception with a missing setting.
    """
    settings.DFP_ORDER_NAME = None
    with self.assertRaises(MissingSettingException):
      tasks.add_new_prebid_partner.main()

  def test_missing_placement_and_ad_units_setting(self, mock_dfp_client):
    """
    It throws an exception with a missing setting.
    """
    settings.DFP_TARGETED_PLACEMENT_NAMES = None
    settings.DFP_TARGETED_AD_UNIT_NAMES = None
    with self.assertRaises(MissingSettingException):
      tasks.add_new_prebid_partner.main()

  def test_missing_bidder_code_setting(self, mock_dfp_client):
    """
    It throws an exception with a missing setting.
    """
    settings.PREBID_BIDDER_CODE = None
    with self.assertRaises(MissingSettingException):
      tasks.add_new_prebid_partner.main()

  @patch('settings.DFP_CURRENCY_CODE', 'EUR', create=True)
  @patch('tasks.add_new_prebid_partner.setup_partner')
  @patch('tasks.add_new_prebid_partner.input', return_value='y')
  def test_custom_currency_code(self, mock_input, mock_setup_partners,
    mock_dfp_client):
    """
    Ensure we use the currency code setting if it exists.
    """
    tasks.add_new_prebid_partner.main()
    args, kwargs = mock_setup_partners.call_args
    self.assertEqual(args[9], 'EUR')

  @patch('settings.DFP_LINE_ITEM_FORMAT', u'{bidder_code}: HB ${price:0>5}', create=True)
  @patch('tasks.add_new_prebid_partner.setup_partner')
  @patch('tasks.add_new_prebid_partner.input', return_value='y')
  def test_custom_line_item_format(self, mock_input, mock_setup_partners,
    mock_dfp_client):
    """
    Ensure we use the line item format setting if it exists.
    """
    tasks.add_new_prebid_partner.main()
    args, kwargs = mock_setup_partners.call_args
    self.assertEqual(args[10], u'{bidder_code}: HB ${price:0>5}')

  def test_price_bucket_validity_missing_key(self, mock_dfp_client):
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

  def test_price_bucket_validity_bad_values(self, mock_dfp_client):
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

  def test_price_bucket_validity_bad_values_again(self, mock_dfp_client):
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
  @patch('tasks.add_new_prebid_partner.input', return_value='n')
  def test_user_confirmation_rejected(self, mock_input, 
    mock_setup_partners, mock_dfp_client):
    """
    Make sure we exit when the user rejects the confirmation.
    """
    tasks.add_new_prebid_partner.main()
    mock_setup_partners.assert_not_called()

  @patch('tasks.add_new_prebid_partner.setup_partner')
  @patch('tasks.add_new_prebid_partner.input', return_value='asdf')
  def test_user_confirmation_not_accepted(self, mock_input, 
    mock_setup_partners, mock_dfp_client):
    """
    Make sure we exit when the user types something other than 'y'.
    """
    tasks.add_new_prebid_partner.main()
    mock_setup_partners.assert_not_called()

  @patch('tasks.add_new_prebid_partner.setup_partner')
  @patch('tasks.add_new_prebid_partner.input', return_value='y')
  def test_user_confirmation_accepted(self, mock_input, 
    mock_setup_partners, mock_dfp_client):
    """
    Make sure we start the process when the user confirms we should proceed.
    """
    tasks.add_new_prebid_partner.main()
    mock_setup_partners.assert_called_once()

  @patch('settings.DFP_NUM_CREATIVES_PER_LINE_ITEM', 5, create=True)
  @patch('tasks.add_new_prebid_partner.setup_partner')
  @patch('tasks.add_new_prebid_partner.input', return_value='y')
  def test_num_duplicate_creatives_from_settings(self, mock_input, 
    mock_setup_partners, mock_dfp_client):
    """
    Make sure we use the settings for the number of creatives per line item
    if the setting exists.
    """
    tasks.add_new_prebid_partner.main()
    args, kwargs = mock_setup_partners.call_args
    num_creatives = args[8]
    self.assertEqual(num_creatives, 5)

  @patch('settings.DFP_NUM_CREATIVES_PER_LINE_ITEM', None, create=True)
  @patch('tasks.add_new_prebid_partner.setup_partner')
  @patch('tasks.add_new_prebid_partner.input', return_value='y')
  def test_num_duplicate_creatives_no_settings_from_placements_and_ad_units(self, mock_input,
    mock_setup_partners, mock_dfp_client):
    """
    Make sure we consider placement and ad units as default number of creatives
    per line item if the setting does not exist.
    """
    tasks.add_new_prebid_partner.main()
    args, kwargs = mock_setup_partners.call_args
    num_creatives = args[8]
    self.assertEqual(num_creatives, len(placements) + len(ad_units))

  @patch('settings.DFP_NUM_CREATIVES_PER_LINE_ITEM', None, create=True)
  @patch('tasks.add_new_prebid_partner.setup_partner')
  @patch('tasks.add_new_prebid_partner.input', return_value='y')
  def test_num_duplicate_creatives_no_settings_from_placements(self, mock_input,
                                               mock_setup_partners, mock_dfp_client):
    """
    Make sure we use placements as the default number of creatives per line item
    if the setting does not exist.
    """
    settings.DFP_TARGETED_AD_UNIT_NAMES = []
    tasks.add_new_prebid_partner.main()
    args, kwargs = mock_setup_partners.call_args
    num_creatives = args[8]
    self.assertEqual(num_creatives, len(placements))

  @patch('settings.DFP_NUM_CREATIVES_PER_LINE_ITEM', None, create=True)
  @patch('tasks.add_new_prebid_partner.setup_partner')
  @patch('tasks.add_new_prebid_partner.input', return_value='y')
  def test_num_duplicate_creatives_no_settings_from_ad_units(self, mock_input,
                                               mock_setup_partners, mock_dfp_client):
    """
    Make sure we use ad units as the default number of creatives per line item
    if the setting does not exist.
    """
    settings.DFP_TARGETED_PLACEMENT_NAMES = []
    tasks.add_new_prebid_partner.main()
    args, kwargs = mock_setup_partners.call_args
    num_creatives = args[8]
    self.assertEqual(num_creatives, len(ad_units))

  @patch('tasks.add_new_prebid_partner.create_line_item_configs')
  @patch('tasks.add_new_prebid_partner.DFPValueIdGetter')
  @patch('tasks.add_new_prebid_partner.get_or_create_dfp_targeting_key')
  @patch('dfp.associate_line_items_and_creatives')
  @patch('dfp.create_creatives')
  @patch('dfp.create_line_items')
  @patch('dfp.create_orders')
  @patch('dfp.get_advertisers')
  @patch('dfp.get_placements')
  @patch('dfp.get_users')
  def test_setup_partner(self, mock_get_users, mock_get_placements,
    mock_get_advertisers, mock_create_orders, mock_create_line_items,
    mock_create_creatives, mock_licas, mock_dfp_client,
    mock_get_or_create_dfp_targeting_key, mock_dfp_value_id_getter,
    mock_create_line_item_configs):
    """
    It calls all expected DFP functions.
    """

    mock_get_users.get_user_id_by_email = MagicMock(return_value=14523)
    mock_get_placements.get_placement_ids_by_name = MagicMock(
      return_value=[1234567, 9876543])
    mock_get_advertisers.get_advertiser_id_by_name = MagicMock(
      return_value=246810)
    mock_create_orders.create_order = MagicMock(return_value=1357913)

    tasks.add_new_prebid_partner.setup_partner(user_email=email, advertiser_name=advertiser, order_name=order,
                                               placements=placements, ad_units=[], sizes=sizes,
                                               bidder_code=bidder_code, prices=prices, num_creatives=2,
                                               currency_code='USD', line_item_format=u'{bidder_code}: HB ${price:0>5}')

    mock_get_users.get_user_id_by_email.assert_called_once_with(email)
    mock_get_placements.get_placement_ids_by_name.assert_called_once_with(
      placements)
    mock_get_advertisers.get_advertiser_id_by_name.assert_called_once_with(
      advertiser)
    mock_create_orders.create_order.assert_called_once_with(order, 246810,
      14523)
    (mock_create_creatives.create_duplicate_creative_configs
      .assert_called_once_with(bidder_code, order, 246810, 2))
    mock_create_creatives.create_creatives.assert_called_once()
    mock_create_line_items.create_line_items.assert_called_once()
    mock_licas.make_licas.assert_called_once()

  def test_create_line_item_configs(self, mock_dfp_client):
    """
    It creates the expected line item configs.
    """

    configs = tasks.add_new_prebid_partner.create_line_item_configs(prices=[100000, 200000, 300000], order_id=1234567,
                                                                    placement_ids=[9876543, 1234567], ad_unit_ids=None,
                                                                    bidder_code='iamabiddr', sizes=[{
            'width': '728',
            'height': '90'
        }], hb_bidder_key_id=999999, hb_pb_key_id=888888, currency_code='HUF',
        line_item_format=u'{bidder_code}: HB ${price:0>5}', HBBidderValueGetter=MagicMock(
            return_value=3434343434), HBPBValueGetter=MagicMock(return_value=5656565656))

    self.assertEqual(len(configs), 3)

    self.assertEqual(configs[0]['name'], 'iamabiddr: HB $00.10')
    self.assertEqual(
      configs[0]['targeting']['inventoryTargeting']['targetedPlacementIds'],
      [9876543, 1234567]
    )
    self.assertEqual(configs[0]['costPerUnit']['microAmount'], 100000)

    self.assertEqual(configs[2]['name'], 'iamabiddr: HB $00.30')
    self.assertEqual(
      configs[2]['targeting']['inventoryTargeting']['targetedPlacementIds'],
      [9876543, 1234567]
    )
    self.assertEqual(configs[2]['costPerUnit']['microAmount'], 300000)
    self.assertEqual(configs[2]['costPerUnit']['currencyCode'], 'HUF')

  @patch('dfp.create_custom_targeting')
  @patch('dfp.get_custom_targeting')
  def test_value_id_getter(self, mock_get_targeting, mock_create_targeting,
    mock_dfp_client):
    """
    It returns the expected values from DFP.
    """

    mock_get_targeting.get_targeting_by_key_name = MagicMock(
      return_value=[
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
    mock_get_targeting.get_key_id_by_name = MagicMock(return_value=987654)
    mock_create_targeting.create_targeting_value = MagicMock(
      return_value=44445555)

    getter = DFPValueIdGetter('some-key-name')

    mock_get_targeting.get_targeting_by_key_name.assert_called_once_with(
      'some-key-name')
    mock_create_targeting.create_targeting_value.assert_not_called()

    # This targeting value already exists.
    self.assertEqual(getter.get_value_id('12.50'), 1324354657)

    # This targeting value does not exist, but we should create it.
    self.assertEqual(getter.get_value_id('15.00'), 44445555)
    mock_create_targeting.create_targeting_value.assert_called_once_with(
      '15.00', 987654)

  @patch('dfp.create_custom_targeting')
  @patch('dfp.get_custom_targeting')
  def test_get_or_create_dfp_targeting_key_does_not_exist(self,
    mock_get_targeting, mock_create_targeting, mock_dfp_client):
    """
    Make sure get_or_create_dfp_targeting_key calls the custom targeting
    module as expected when a targeting key does not exist.
    """

    # Mock that the key does not exist in DFP
    mock_get_targeting.get_key_id_by_name = MagicMock(return_value=None)
    mock_create_targeting.create_targeting_key = MagicMock()

    tasks.add_new_prebid_partner.get_or_create_dfp_targeting_key('my-key')

    (mock_get_targeting.get_key_id_by_name
      .assert_called_once_with('my-key'))
    (mock_create_targeting.create_targeting_key
      .assert_called_once_with('my-key'))

  @patch('dfp.create_custom_targeting')
  @patch('dfp.get_custom_targeting')
  def test_get_or_create_dfp_targeting_key_exists(self,
    mock_get_targeting, mock_create_targeting, mock_dfp_client):
    """
    Make sure get_or_create_dfp_targeting_key calls the custom targeting
    module as expected when a targeting key exists.
    """

    mock_get_targeting.get_key_id_by_name = MagicMock(
      return_value=[
        {
          'customTargetingKeyId': 987654,
          'displayName': 'some-key',
          'id': 1324354657,
          'name': 'Some other key'
        }
      ]
    )
    mock_create_targeting.create_targeting_key = MagicMock()

    tasks.add_new_prebid_partner.get_or_create_dfp_targeting_key('some-key')

    mock_get_targeting.get_key_id_by_name.assert_called_once_with('some-key')
    mock_create_targeting.create_targeting_key.assert_not_called()

  def test_logging_unicode(self, mock_dfp_client):
    """
    We can log unicode.
    """
    tasks.add_new_prebid_partner.logger.info(u'Hi there!')
    tasks.add_new_prebid_partner.logger.info(u'\xe4')
    tasks.add_new_prebid_partner.logger.info(
      u"""A with umlaut: {my_character}""".format(my_character=u'\xe4'))

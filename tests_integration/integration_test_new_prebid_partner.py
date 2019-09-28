
import os
from datetime import datetime
from mock import patch
from unittest import TestCase

import settings
import tasks.add_new_prebid_partner
from tests_integration.helpers.archive_order_by_name import archive_order_by_name
from tests_integration.helpers.get_advertiser_by_name import get_advertiser_by_name
from tests_integration.helpers.get_custom_targeting_by_key_name import (
  get_custom_targeting_by_key_name,
  get_key_by_name
)
from tests_integration.helpers.get_line_items_for_order import get_line_items_for_order
from tests_integration.helpers.get_order_by_name import get_order_by_name
from tests_integration.helpers.get_placement_by_name import get_placement_by_name

now = datetime.now().isoformat()

# Note: these tests expect that the live DFP network has preexisting
# trafficker, advertiser, and placements.
email = os.environ['INTEGRATION_TEST_TRAFFICKER_EMAIL']
advertiser = 'TestAdvertiser'
order_name = 'Test Order: {now}'.format(now=now)
placements = [
  'My Placement #1',
  'My Placement #2'
]
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
bidder_code = 'testbidder'
price_buckets = {
  'precision': 2,
  'min' : 0,
  'max' : 20,
  'increment': 0.10,
}

class NewPrebidPartnerTests(TestCase):

  def setUp(self):
    pass

  def tearDown(self):
    print('Cleaning up: archiving the order and deleting custom targeting key-values.')

    # Archive the order we created for this test
    archive_order_by_name(order_name)

    # TODO: delete custom targeting keys and values
    # https://developers.google.com/doubleclick-publishers/docs/reference/v201908/CustomTargetingService.DeleteCustomTargetingKeys
    # https://developers.google.com/doubleclick-publishers/docs/reference/v201908/CustomTargetingService.DeleteCustomTargetingValues

  @patch.multiple('settings',
    DFP_USER_EMAIL_ADDRESS=email,
    DFP_ADVERTISER_NAME=advertiser,
    DFP_ORDER_NAME=order_name,
    DFP_TARGETED_PLACEMENT_NAMES=placements,
    DFP_PLACEMENT_SIZES = sizes,
    PREBID_BIDDER_CODE=bidder_code,
    PREBID_PRICE_BUCKETS=price_buckets,
    DFP_CREATE_ADVERTISER_IF_DOES_NOT_EXIST=False,
    DFP_USE_EXISTING_ORDER_IF_EXISTS=False)
  @patch('tasks.add_new_prebid_partner.input', return_value='y')
  def test_new_partner(self, mock_input):
    # Add new bidder partner
    print('Creating new bidder partner...')
    tasks.add_new_prebid_partner.main()
    print('New bidder partner created.')
    print('Fetching created order and line items...')

    # Get the order and check that the order and line items
    # match what we'd expect.
    order = get_order_by_name(order_name)
    if order is None:
      self.fail('Order was not created.')

    # Validate the order
    self.assertEqual(order['name'], order_name)
    self.assertEqual(order['status'], 'DRAFT')
    self.assertEqual(order['isArchived'], False)
    expected_advertiser = get_advertiser_by_name(advertiser)
    self.assertEqual(order['advertiserId'], expected_advertiser['id'])

    # Make sure line items match what we expect
    line_items = get_line_items_for_order(order['id'])
    sorted_line_items = sorted(line_items, key=lambda li: li['costPerUnit']['microAmount'])
    # print(sorted_line_items[0:2])
    print('Validating line items...')

    # Fetch expected values from DFP
    expected_placement_ids = [
      get_placement_by_name(placements[0])['id'],
      get_placement_by_name(placements[1])['id']
    ]
    hb_bidder_key = get_key_by_name('hb_bidder')
    hb_pb_key = get_key_by_name('hb_pb')
    hb_bidder_vals = get_custom_targeting_by_key_name('hb_bidder')
    expected_bidder_val = next(filter(
      lambda hb_bidders: hb_bidders['name'] == bidder_code,
      hb_bidder_vals))
    hb_pb_vals = get_custom_targeting_by_key_name('hb_pb')
    sorted_hb_pb_vals = sorted(hb_pb_vals, key=lambda pb: float(pb['name']))
    num_line_items = 201
    cpm_micro_amouts = list(map(lambda x: x * (10**5), range(num_line_items)))
    self.assertEqual(len(sorted_line_items), num_line_items)

    # Check each line item
    for index, li in enumerate(sorted_line_items):
      micro_amount = cpm_micro_amouts[index]
      hb_pb_val = sorted_hb_pb_vals[index]
      usd_val = float(micro_amount) / 10**6
      usd_string = '%.{0}f'.format(str(2)) % usd_val

      # print('Validating line item targeting hb_pb = {0}'.format(usd_string))

      # Line item name
      expected_name = 'testbidder: HB ${0}'.format(usd_string)
      self.assertEqual(li['name'], expected_name)

      # CPM
      self.assertEqual(li['costPerUnit']['currencyCode'], 'USD')
      self.assertEqual(li['costPerUnit']['microAmount'], micro_amount)

      # Creative placeholders
      creative_placeholders = sorted(li['creativePlaceholders'],
        key=lambda cp: cp['size']['width'])
      self.assertEqual(len(creative_placeholders), 2)
      self.assertEqual(creative_placeholders[0]['size']['width'], 300)
      self.assertEqual(creative_placeholders[0]['size']['height'], 250)
      self.assertEqual(creative_placeholders[1]['size']['width'], 728)
      self.assertEqual(creative_placeholders[1]['size']['height'], 90)

      # Status
      # TODO: eventually should have the tool activate line items
      self.assertEqual(li['status'], 'DRAFT')
      self.assertEqual(li['isArchived'], False)

      # Targeting
      targ = li['targeting']
      self.assertEqual(targ['geoTargeting'], None)
      self.assertEqual(targ['inventoryTargeting']['targetedAdUnits'], [])
      self.assertEqual(targ['inventoryTargeting']['excludedAdUnits'], [])
      self.assertEqual(targ['inventoryTargeting']['targetedPlacementIds'],
        expected_placement_ids)

      # Check that custom targeting keys and values are correct
      self.assertEqual(
        targ['customTargeting']['children'][0]['logicalOperator'],
        'AND')
      # The first statement with an "AND" operator.
      custom_targ_logic = targ['customTargeting']['children'][0]['children']
      self.assertEqual(len(custom_targ_logic), 2)
      custom_targ_hb_bidder = next(filter(
        lambda ct: ct['keyId'] == hb_bidder_key['id'],
        custom_targ_logic))
      custom_targ_hb_pb = next(filter(
        lambda ct: ct['keyId'] == hb_pb_key['id'],
        custom_targ_logic))

      # All line items should be targeted to the same hb_bidder value
      self.assertEqual(custom_targ_hb_bidder['operator'], 'IS')
      self.assertEqual(custom_targ_hb_bidder['valueIds'], [expected_bidder_val['id']])

      # Each line item should be targeted to its own hb_pb value
      self.assertEqual(custom_targ_hb_pb['operator'], 'IS')
      self.assertEqual(custom_targ_hb_pb['valueIds'], [hb_pb_val['id']])
      # The hb_pb value should have the same name as the CPM value
      self.assertEqual(hb_pb_val['name'], usd_string)
      self.assertEqual(hb_pb_val['displayName'], usd_string)

    print('Line items validated.')


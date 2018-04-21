
import os
from datetime import datetime
from mock import patch
from unittest import TestCase

import settings
from tests_integration.helpers.get_line_items_for_order import get_line_items_for_order
from tests_integration.helpers.get_order_by_name import get_order_by_name
from tests_integration.helpers.get_placement_by_name import get_placement_by_name

now = datetime.now().isoformat()

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
    # TODO: archive order
    # TODO: delete custom targeting keys and values
    pass

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
  def test_new_partner(self):

    # TODO: add new bidder partner
    print('Creating new bidder partner...')
    print('New bidder partner created.')
    print('Fetching created order and line items...')

    # Get the order and check that the order and line items
    # match what we'd expect.
    # TODO: use generated order name
    order = get_order_by_name('Test April 5 2018')
    if order is None:
      self.fail('Order was not created.')

    # Validate the order
    self.assertEqual(order['name'], 'Test April 5 2018')
    self.assertEqual(order['status'], 'DRAFT')
    # TODO: check advertiser ID

    line_items = get_line_items_for_order(order['id'])
    sorted_line_items = sorted(line_items, key=lambda li: li['costPerUnit']['microAmount'])

    placement_ids = [
      get_placement_by_name(placements[0])['id'],
      get_placement_by_name(placements[1])['id']
    ]

    # Make sure line items match what we expect
    print('Validating line items...')
    # print(sorted_line_items[0:2])

    num_line_items = 201
    cpm_micro_amouts = map(lambda x: x * (10**5), range(num_line_items))
    self.assertEqual(len(sorted_line_items), num_line_items)

    for index, li in enumerate(sorted_line_items):
      micro_amount = cpm_micro_amouts[index]

      # Line item name
      usd_val = float(micro_amount) / 10**6
      usd_string = '%.{0}f'.format(str(2)) % usd_val
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
      # TODO: reenable (some current test orders are archived)
      # self.assertEqual(li['isArchived'], False)

      # Targeting
      targ = li['targeting']
      self.assertEqual(targ['geoTargeting'], None)
      self.assertEqual(targ['inventoryTargeting']['targetedAdUnits'], [])
      self.assertEqual(targ['inventoryTargeting']['excludedAdUnits'], [])
      self.assertEqual(targ['inventoryTargeting']['targetedPlacementIds'],
        placement_ids)

      # TODO
      # Check that custom targeting keys and values are correct

    print('Line items validated.')



import os
from datetime import datetime
from mock import patch
from unittest import TestCase

import settings
from tests_integration.helpers.get_line_items_for_order import get_line_items_for_order
from tests_integration.helpers.get_order_by_name import get_order_by_name

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

    # Get the order and check that the order and line items
    # match what we'd expect.
    order = get_order_by_name('Test April 5 2018')
    if order is None:
      self.fail('Order was not created.')
    line_items = get_line_items_for_order(order['id'])

    # TODO: check line items' structure
    print(line_items[0:4])

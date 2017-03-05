#!/usr/bin/env python

import settings
import dfp.create_orders
import dfp.get_advertisers
import dfp.get_users
from dfp.exceptions import (
  BadSettingException,
  MissingSettingException
)
from tasks.price_utils import (
  get_prices_array,
  get_prices_summary_string,
)

# TODO: Change all print statements to logging and add logging flag.
# TODO: Disable logging during tests.

def setup_partner(user_email, advertiser_name, order_name, placements,
    bidder_code, price_buckets):
  """
  Call all necessary DfP tasks for a new Prebid partner setup.
  """

  # Get the user.
  user_id = dfp.get_users.get_user_id_by_email(user_email)

  # Get (or potentially create) the advertiser.
  advertiser_id = dfp.get_advertisers.get_advertiser_id_by_name(
    advertiser_name)

  # Create the order.
  dfp.create_orders.create_order(order_name, advertiser_id, user_id)

  # TODO: line items, creatives, targeting

def check_price_buckets_validity(price_buckets):
  """
  Validate that the price_buckets object contains all required keys and the
  values are the expected types.

  Args:
    price_buckets (object)
  Returns:
    None
  """

  try:
    pb_precision = price_buckets['precision']
    pb_min = price_buckets['min']
    pb_max = price_buckets['max']
    pb_increment = price_buckets['increment']
  except KeyError:
    raise BadSettingException('The setting "PREBID_PRICE_BUCKETS" '
      'must contain keys "precision", "min", "max", and "increment".')
  
  if not (isinstance(pb_precision, int) or isinstance(pb_precision, float)):
    raise BadSettingException('The "precision" key in "PREBID_PRICE_BUCKETS" '
      'must be a number.')

  if not (isinstance(pb_min, int) or isinstance(pb_min, float)):
    raise BadSettingException('The "min" key in "PREBID_PRICE_BUCKETS" '
      'must be a number.')

  if not (isinstance(pb_max, int) or isinstance(pb_max, float)):
    raise BadSettingException('The "max" key in "PREBID_PRICE_BUCKETS" '
      'must be a number.')

  if not (isinstance(pb_increment, int) or isinstance(pb_increment, float)):
    raise BadSettingException('The "increment" key in "PREBID_PRICE_BUCKETS" '
      'must be a number.')

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def main():
  """
  Validate the settings and ask for confirmation from the user. Then,
  start all necessary DFP tasks.
  """

  user_email = getattr(settings, 'DFP_USER_EMAIL_ADDRESS', None)
  if user_email is None:
    raise MissingSettingException('DFP_USER_EMAIL_ADDRESS')
   
  advertiser_name = getattr(settings, 'DFP_ADVERTISER_NAME', None)
  if advertiser_name is None:
    raise MissingSettingException('DFP_ADVERTISER_NAME')

  order_name = getattr(settings, 'DFP_ORDER_NAME', None)
  if order_name is None:
    raise MissingSettingException('DFP_ORDER_NAME')

  placements = getattr(settings, 'DFP_TARGETED_PLACEMENT_IDS', None)
  if placements is None:
    raise MissingSettingException('DFP_TARGETED_PLACEMENT_IDS')
  elif len(placements) < 1:
    raise BadSettingException('The setting "DFP_TARGETED_PLACEMENT_IDS" '
      'must contain at least one DFP placement ID.')

  bidder_code = getattr(settings, 'PREBID_BIDDER_CODE', None)
  if bidder_code is None:
    raise MissingSettingException('PREBID_BIDDER_CODE')

  price_buckets = getattr(settings, 'PREBID_PRICE_BUCKETS', None)
  if price_buckets is None:
    raise MissingSettingException('PREBID_PRICE_BUCKETS')

  check_price_buckets_validity(price_buckets)

  prices = get_prices_array(price_buckets)
  prices_summary = get_prices_summary_string(prices)

  print """

    Going to create {name_start_format}{num_line_items}{format_end} new line items.
      {name_start_format}Order{format_end}: {value_start_format}{order_name}{format_end}
      {name_start_format}Advertiser{format_end}: {value_start_format}{advertiser}{format_end}
      {name_start_format}Owner{format_end}: {value_start_format}{user_email}{format_end}

    Line items will have targeting:
      {name_start_format}hb_pb{format_end} = {value_start_format}{prices_summary}{format_end}
      {name_start_format}hb_bidder{format_end} = {value_start_format}{bidder_code}{format_end}
      {name_start_format}placements{format_end} = {value_start_format}{placements}{format_end}

    """.format(
      num_line_items = len(prices),
      order_name=order_name,
      advertiser=advertiser_name,
      user_email=user_email,
      prices_summary=prices_summary,
      bidder_code=bidder_code,
      placements=placements,
      name_start_format=color.BOLD,
      format_end=color.END,
      value_start_format=color.BLUE,
    )

  ok = raw_input('Is this correct? (y/n)\n')

  if ok != 'y':
    print 'Exiting.'
    return

  setup_partner(
    user_email,
    advertiser_name,
    order_name,
    placements,
    bidder_code,
    price_buckets
  )

if __name__ == '__main__':
  main()

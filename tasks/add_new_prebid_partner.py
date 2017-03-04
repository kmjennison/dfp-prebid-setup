#!/usr/bin/env python

import settings
import dfp.create_orders
import dfp.get_advertisers
import dfp.get_users


def main():

  user_email = getattr(settings, 'DFP_USER_EMAIL_ADDRESS', None)
  if user_email is None:
    raise MissingSettingException('DFP_USER_EMAIL_ADDRESS')
   
  advertiser_name = getattr(settings, 'DFP_ADVERTISER_NAME', None)
  if advertiser_name is None:
    raise MissingSettingException('DFP_ADVERTISER_NAME')

  order_name = getattr(settings, 'DFP_ORDER_NAME', None)
  if order_name is None:
    raise MissingSettingException('DFP_ORDER_NAME')

  print """
    Going to create a new order in DFP called "{order_name}"
    for advertiser "{advertiser}", owned by user {user_email}.
    """.format(
      order_name=order_name,
      advertiser=advertiser_name,
      user_email=user_email
    )

  ok = raw_input('Is this correct? (y/n)\n')

  if ok != 'y':
    print 'Exiting.'
    return

  # Get the user.
  user_id = dfp.get_users.get_user_id_by_email(user_email)

  # Get (or potentially create) the advertiser.
  advertiser_id = dfp.get_advertisers.get_advertiser_id_by_name(
    advertiser_name)

  # Create the order.
  dfp.create_orders.create_order(order_name, advertiser_id, user_id)

  # TODO: line items, creatives, targeting

if __name__ == '__main__':
  main()

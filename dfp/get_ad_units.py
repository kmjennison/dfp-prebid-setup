#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from googleads import dfp

from dfp.client import get_client


logger = logging.getLogger(__name__)

def get_all_ad_units(print_ad_units=False):
  """
  Gets ad units from DFP.

  Returns:
    array of ad units
  """

  # Initialize units array
  ad_units = []

  dfp_client = get_client()

  # Initialize appropriate service.
  ad_unit_service = dfp_client.GetService('InventoryService', version='v201802')

  # Create a statement to select ad units.
  statement = dfp.StatementBuilder()

  # Retrieve a small amount of ad units at a time, paging
  # through until all ad units have been retrieved.
  while True:
    response = ad_unit_service.getAdUnitsByStatement(statement.ToStatement())
    if 'results' in response:
      for ad_unit in response['results']:
        ad_units.append(ad_unit)
        if print_ad_units:
          print('Ad unit with ID "%s" and name "%s" was found.' % (ad_unit['id'], ad_unit['name']))
      statement.offset += dfp.SUGGESTED_PAGE_LIMIT
    else:
      break

  return ad_units

def main():
  get_all_ad_units(print_ad_units=True)

if __name__ == '__main__':
  main()
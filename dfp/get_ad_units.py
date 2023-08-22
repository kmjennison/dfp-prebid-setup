#!/usr/bin/env python

import logging

from googleads import ad_manager

import settings
from dfp.client import get_client
from dfp.exceptions import (
  BadSettingException,
  DFPObjectNotFound,
  MissingSettingException
)


logger = logging.getLogger(__name__)

def get_ad_unit_by_name(ad_unit_name):
  """
  Gets a ad unit by name from DFP.

  Args:
    ad_unit_name (str): the name of the DFP ad unit
  Returns:
    a DFP ad unit object
  """

  dfp_client = get_client()
  ad_unit_service = dfp_client.GetService('InventoryService',
    version='v202305')

  query = 'WHERE name = :name'
  values = [
      {'key': 'name',
       'value': {
           'xsi_type': 'TextValue',
           'value': ad_unit_name
       }},
  ]
  statement = ad_manager.FilterStatement(query, values)
  response = ad_unit_service.getAdUnitsByStatement(
    statement.ToStatement())

  no_ad_unit_found = False
  try:
    no_ad_unit_found = True if len(response['results']) < 1 else False 
  except (AttributeError, KeyError):
    no_ad_unit_found = True

  if no_ad_unit_found:
    raise DFPObjectNotFound('No DFP ad_unit found with name {0}'.format(
      ad_unit_name))
  else:
    ad_unit = response['results'][0]
    logger.info(u'Found ad_unit with name "{name}".'.format(name=ad_unit['name']))
  return ad_unit

def get_ad_unit_ids_by_name(ad_unit_names):
  """
  Gets ad unit IDs from DFP based on their names.

  Args:
    ad_unit_names (arr): an array of ad unit name strings
  Returns:
    an array: an array of ad unit IDs
  """  
  ad_unit_ids = []
  for ad_unit_name in ad_unit_names:
    ad_unit_ids.append(get_ad_unit_by_name(ad_unit_name)['id'])
  return ad_unit_ids

def main():
  """
  Loads ad units from settings and fetches them from DFP.

  Returns:
    None
  """  

  ad_units = getattr(settings, 'DFP_TARGETED_AD_UNIT_NAMES', None)
  if ad_units is None:
    raise MissingSettingException('DFP_TARGETED_AD_UNIT_NAMES')
  elif len(ad_units) < 1:
    raise BadSettingException('The setting "DFP_TARGETED_AD_UNIT_NAMES" '
      'must contain at least one ad unit ID.')

  get_ad_unit_ids_by_name(ad_units)

if __name__ == '__main__':
  main()

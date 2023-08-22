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

def get_placement_by_name(placement_name):
  """
  Gets a placement by name from DFP.

  Args:
    placement_name (str): the name of the DFP placement
  Returns:
    a DFP placement object
  """

  dfp_client = get_client()
  placement_service = dfp_client.GetService('PlacementService',
    version='v202305')

  query = 'WHERE name = :name'
  values = [
      {'key': 'name',
       'value': {
           'xsi_type': 'TextValue',
           'value': placement_name
       }},
  ]
  statement = ad_manager.FilterStatement(query, values)
  response = placement_service.getPlacementsByStatement(
    statement.ToStatement())

  no_placement_found = False
  try:
    no_placement_found = True if len(response['results']) < 1 else False 
  except (AttributeError, KeyError):
    no_placement_found = True

  if no_placement_found:
    raise DFPObjectNotFound('No DFP placement found with name {0}'.format(
      placement_name))
  else:
    placement = response['results'][0]
    logger.info(u'Found placement with name "{name}".'.format(name=placement['name']))
  return placement

def get_placement_ids_by_name(placement_names):
  """
  Gets placement IDs from DFP based on their names.

  Args:
    placement_names (arr): an array of placement name strings
  Returns:
    an array: an array of placement IDs
  """  
  placement_ids = []
  for placement_name in placement_names:
    placement_ids.append(get_placement_by_name(placement_name)['id'])
  return placement_ids

def main():
  """
  Loads placements from settings and fetches them from DFP.

  Returns:
    None
  """  

  placements = getattr(settings, 'DFP_TARGETED_PLACEMENT_NAMES', None)
  if placements is None:
    raise MissingSettingException('DFP_TARGETED_PLACEMENT_NAMES')
  elif len(placements) < 1:
    raise BadSettingException('The setting "DFP_TARGETED_PLACEMENT_NAMES" '
      'must contain at least one placement ID.')

  get_placement_ids_by_name(placements)

if __name__ == '__main__':
  main()

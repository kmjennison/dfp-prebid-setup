#!/usr/bin/env python

import logging

from googleads import ad_manager

from dfp.client import get_client

def get_placement_by_name(placement_name):
  """
  Gets a placement by name from DFP.

  Args:
    placement_name (str): the name of the DFP placement
  Returns:
    a DFP placement object
  """

  client = get_client()
  placement_service = client.GetService('PlacementService',
    version='v202008')

  statement = (ad_manager.StatementBuilder()
    .Where('name = :name')
    .WithBindVariable('name', placement_name))
  response = placement_service.getPlacementsByStatement(
    statement.ToStatement())

  if 'results' in response and len(response['results']) > 0:
    return response['results'][0]
  else:
    return None

#!/usr/bin/env python

import logging

from googleads import ad_manager

from dfp.client import get_client

def get_key_by_name(key_name):
  """
  Gets a targeting key by key name.

  Args:
    name (str): the name of the targeting key
  Returns:
    the key object
  """

  client = get_client()
  custom_targeting_service = client.GetService('CustomTargetingService',
    version='v201811')

  statement = (ad_manager.StatementBuilder()
    .Where('name = :name')
    .WithBindVariable('name', key_name))
  response = custom_targeting_service.getCustomTargetingKeysByStatement(
      statement.ToStatement())

  if 'results' in response and len(response['results']) > 0:
    return response['results'][0]
  else:
    return None

def get_custom_targeting_by_key_name(key_name):
  """
  Gets a set of custom targeting values by key name

  Args:
    name (str): the name of the targeting key
  Returns:
    an array, or None: if the key exists, return an array of objects, where
      each object is info about a custom targeting value
  """

  key_id = get_key_by_name(key_name)['id']

  client = get_client()
  custom_targeting_service = client.GetService('CustomTargetingService',
    version='v201811')

  statement = (ad_manager.StatementBuilder()
    .Where('customTargetingKeyId = :customTargetingKeyId')
    .WithBindVariable('customTargetingKeyId', key_id))
  response = custom_targeting_service.getCustomTargetingValuesByStatement(
    statement.ToStatement())

  vals = []
  while True:
    response = custom_targeting_service.getCustomTargetingValuesByStatement(
        statement.ToStatement())
    if 'results' in response and len(response['results']) > 0:
      vals = vals + response['results']
      statement.offset += statement.limit
    else:
      break
  return vals

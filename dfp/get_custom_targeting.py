#!/usr/bin/env python

from googleads import dfp

from dfp.client import get_client


def get_key_id_by_name(name):
  """
  Gets a targeting key by key name.

  Args:
    name (str): the name of the targeting key
  Returns:
    an integer, or None
  """

  dfp_client = get_client()
  custom_targeting_service = dfp_client.GetService('CustomTargetingService',
    version='v201702')

  # Get a key by name.
  query = ('WHERE name = :name')
  values = [{
    'key': 'name',
    'value': {
      'xsi_type': 'TextValue',
      'value': name
    }
  }]
  targeting_key_statement = dfp.FilterStatement(query, values)

  response = custom_targeting_service.getCustomTargetingKeysByStatement(
      targeting_key_statement.ToStatement())

  key = None
  if 'results' in response:
    key = response['results'][0]

  return key['id']


def get_targeting_by_key_name(name):
  """
  Gets a set of custom targeting values by key name

  Args:
    name (str): the name of the targeting key
  Returns:
    an array, or None: if the key exists, return an array of objects, where
      each object is info about a custom targeting value
  """

  dfp_client = get_client()
  custom_targeting_service = dfp_client.GetService('CustomTargetingService',
    version='v201702')

  # Get a key by name.
  query = ('WHERE name = :name')
  values = [{
    'key': 'name',
    'value': {
      'xsi_type': 'TextValue',
      'value': name
    }
  }]
  targeting_key_statement = dfp.FilterStatement(query, values)

  response = custom_targeting_service.getCustomTargetingKeysByStatement(
      targeting_key_statement.ToStatement())

  # If the key exists, get predefined values.
  key_values = None
  if 'results' in response:
    key = response['results'][0]
    key_values = []

    query = 'WHERE customTargetingKeyId IN (%s)' % str(key['id'])
    statement = dfp.FilterStatement(query)

    response = custom_targeting_service.getCustomTargetingValuesByStatement(
        statement.ToStatement())
    if 'results' in response:
      for custom_val in response['results']:
        key_values.append({
          'id': custom_val['id'],
          'name': custom_val['name'],
          'displayName': custom_val['displayName'],
          'customTargetingKeyId': custom_val['customTargetingKeyId']
        })
      statement.offset += dfp.SUGGESTED_PAGE_LIMIT

  if key_values is None:
    print 'Key {key_name} does not exist in DFP.'. format(key_name=name)
  elif len(key_values) < 1:
    print 'Key {key_name} exists but has no custom values.'. format(
      key_name=name)
  else:
    print 'Key {key_name} exists and has {num} custom values.'. format(
      key_name=name, num=len(key_values))

  return key_values

def main():
  get_targeting_by_key_name('hb_bidder')
  get_targeting_by_key_name('hb_pb')

if __name__ == '__main__':
  main()

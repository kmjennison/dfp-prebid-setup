#!/usr/bin/env python

from googleads import dfp

from dfp.client import get_client


def create_targeting_key(name, display_name, key_type='FREEFORM'):
  """
  Creates a custom targeting key in DFP.

  Args:
    name (str): the name of the targeting key
    display_name (str)
    type (str): either 'FREEFORM' or 'PREDEFINED'
  Returns:
    an integer: the ID of the created key
  """

  dfp_client = get_client()
  custom_targeting_service = dfp_client.GetService('CustomTargetingService',
    version='v201702')

  # Create custom targeting key objects.
  keys = [
    {
      'displayName': display_name,
      'name': name,
      'type': key_type
    }
  ]

  # Add custom targeting keys.
  keys = custom_targeting_service.createCustomTargetingKeys(keys)
  key = keys[0]

  print ('Created a custom targeting key with id \'%s\', name \'%s\', and '
         'display name \'%s\'.' % (key['id'], key['name'], key['displayName']))

  return key['id']

def create_targeting_value(name, key_id):
  """
  Creates a custom targeting value for a specific key in DFP.

  Args:
    name (str): the name of value
    key_id (int): the ID of the associated DFP key
  Returns:
    None
  """

  dfp_client = get_client()
  custom_targeting_service = dfp_client.GetService('CustomTargetingService',
    version='v201702')

  values_config = [
    {
      'customTargetingKeyId': key_id,
      'displayName': str(name),
      'name': str(name),
      'matchType': 'EXACT'
    }
  ]

  # Add custom targeting values.
  if len(values_config) > 0:
    values = custom_targeting_service.createCustomTargetingValues(
      values_config)

  # Display results.
  if values:
    created_value = values[0]

  print ('A custom targeting value with id \'%s\', belonging to key with id'
         ' \'%s\', name \'%s\', and display name \'%s\' was created.'
         % (created_value['id'], created_value['customTargetingKeyId'],
            created_value['name'], created_value['displayName']))

  return created_value['id']

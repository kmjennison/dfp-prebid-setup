#!/usr/bin/env python

import logging

from googleads import ad_manager

import settings
from dfp.client import get_client
from dfp.exceptions import DFPObjectNotFound, MissingSettingException


logger = logging.getLogger(__name__)

def get_user_id_by_email(email_address):
  """
  Returns a DFP user ID from email address.

  Args:
    email (str): the email of the DFP user
  Returns:
    an integer: the user's DFP ID
  """
  dfp_client = get_client()
  user_service = dfp_client.GetService('UserService', version='v202305')

  # Filter by email address.
  query = 'WHERE email = :email'
  values = [
      {'key': 'email',
       'value': {
           'xsi_type': 'TextValue',
           'value': email_address
       }},
  ]
  statement = ad_manager.FilterStatement(query, values)

  response = user_service.getUsersByStatement(statement.ToStatement())

  # A user is required.
  no_user_found = False
  try:
    no_user_found = True if len(response['results']) < 1 else False 
  except (AttributeError, KeyError):
    no_user_found = True

  if no_user_found:
    raise DFPObjectNotFound('No DFP user found with given email address.')

  # Only get the first user in case there are multiple matches.
  user = response['results'][0]

  logger.info(u'Found user with the given email address.')

  return user['id']

def main():
  """
  Gets user email address from settings and fetches the user.

  Returns:
    an integer: the user's DFP ID
  """  

  email = getattr(settings, 'DFP_USER_EMAIL_ADDRESS', None)
  if email is None:
    raise MissingSettingException('DFP_USER_EMAIL_ADDRESS')

  return get_user_id_by_email(email)

if __name__ == '__main__':
  main()

#!/usr/bin/env python

import logging

from googleads import ad_manager

from dfp.client import get_client

def get_advertiser_by_name(advertiser_name):
  """
  Returns a DFP company ID from company name.

  Args:
    name (str): the name of the DFP advertiser
  Returns:
    an integer: the advertiser's DFP ID
  """

  client = get_client()
  company_service = client.GetService('CompanyService',
    version='v202008')

  statement = (ad_manager.StatementBuilder()
    .Where('name = :name')
    .WithBindVariable('name', advertiser_name))
  response = company_service.getCompaniesByStatement(
    statement.ToStatement())

  if 'results' in response and len(response['results']) > 0:
    return response['results'][0]
  else:
    return None

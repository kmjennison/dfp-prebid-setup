import pdb
import yaml
from googleads import dfp
from googleads import oauth2

with open('googleads.yaml', 'r') as stream:
  try:
    config = yaml.load(stream)
  except yaml.YAMLError as e:
    print(e)
    print 'Could not load configuration from googleads.yaml. Exiting.'
    quit()

try:
  service_account_email = config['dfp']['service_account_email']
  key_file_path = config['dfp']['path_to_private_key_file']
  application_name = config['dfp']['application_name']
except KeyError:
  print 'Missing required configuration in googleads.yaml file.'
  quit()

# Initialize the GoogleRefreshTokenClient.
oauth2_client = oauth2.GoogleServiceAccountClient(
  oauth2.GetAPIScope('dfp'), service_account_email, key_file_path)

# Initialize the DFP client.
dfp_client = dfp.DfpClient(oauth2_client, application_name)

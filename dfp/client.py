
from googleads import dfp

import settings
from settings import GOOGLEADS_YAML_FILE


def get_client():
  print('Settings module file path:')
  print(settings.GOOGLEADS_YAML_FILE)

  print('Imported file path:')
  print(GOOGLEADS_YAML_FILE)
  return dfp.DfpClient.LoadFromStorage(GOOGLEADS_YAML_FILE)

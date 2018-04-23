
from googleads import dfp

import settings


def get_client():
  print('Settings module file path:')
  return dfp.DfpClient.LoadFromStorage(settings.GOOGLEADS_YAML_FILE)


from googleads import dfp

import settings


def get_client():
  return dfp.DfpClient.LoadFromStorage(settings.GOOGLEADS_YAML_FILE)

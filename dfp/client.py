
from googleads import ad_manager

import settings


def get_client():
  return ad_manager.AdManagerClient.LoadFromStorage(settings.GOOGLEADS_YAML_FILE)

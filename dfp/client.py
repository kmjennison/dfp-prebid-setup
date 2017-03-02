
from googleads import dfp

from settings import GOOGLEADS_YAML_FILE


def get_client():
  return dfp.DfpClient.LoadFromStorage(GOOGLEADS_YAML_FILE)

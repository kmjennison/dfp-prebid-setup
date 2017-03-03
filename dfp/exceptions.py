
class MissingSettingException(Exception):
  def __init__(self, message, *args):
    detailed_message = (
      'Missing required setting {0} in settings.py'.format(message))
    super(MissingSettingException, self).__init__(detailed_message, *args) 
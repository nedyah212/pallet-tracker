class HelperMethods():

  def boolean_to_status_string(self, boolean):
    return "At Capacity" if boolean else "Not at Capacity" if boolean is not None else ''

  @staticmethod
  def remove_delimiters(text):
    return text.replace('-', '').replace(' ', '').replace('/', '') if text is not None else ''
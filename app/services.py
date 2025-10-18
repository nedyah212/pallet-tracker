class HelperMethods():

  def boolean_to_status_string(self, boolean):
    return "At Capacity" if boolean else "Not at Capacity"

  @staticmethod
  def remove_delimiters(text):
    return text.replace('-', '').replace(' ', '').replace('/', '')
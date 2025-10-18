import re

class HelperMethods():

  def boolean_to_status_string(self, boolean):
    return "At Capacity" if boolean else "Not at Capacity"

  def remove_delimiters(text):
      return re.sub(r'[-\s]', '', text)
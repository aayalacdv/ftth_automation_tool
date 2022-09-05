
class element_text_not_null(object):
  """
    An expectation for cheking a text value is not null

  """
  def __init__(self, element):
    self.element = element 

  def __call__(self, driver):

    if len(self.element.get_attribute("value").strip()) != 0:
        return self.element
    else:
        return False
class DoesNotFollowRulesException(Exception):
  def __init__(message: str):
    self.message = message
    super().__init__(self.message)

class DoesNotContainTableException(Exception):
  def __init__(message: str):
    self.message = message
    super().__init__(self.message)
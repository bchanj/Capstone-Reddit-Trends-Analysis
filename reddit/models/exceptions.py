class DoesNotFollowRules(Exception):
  def __init__(message: str):
    self.message = message
    super().__init__(self.message)

class DoesNotContainTable(Exception):
  def __init__(message: str):
    self.message = message
    super().__init__(self.message)
import sys
sys.path.append(os.path.dirname(__file__))

class QueryFilter():
    def __init__(self, key, value):
        self.key = key
        self.value = value
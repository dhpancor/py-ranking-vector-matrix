class NoResolver:
    """
    This class is intended to be used when no resolver is needed or available.
    """

    def process_preference(self, value):
        return value

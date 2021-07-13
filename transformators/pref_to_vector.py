from schemas.tweet import Tweet


class PrefToVector:

    def __init__(self, preferences):
        """
        This class transforms all the tweets stored in the database
        into a dictionary of vectors of preferences identified
        by tweet ID.
        :param preferences: the list of the preferences.
        """
        self.preferences = preferences
        self.results = {}
        self.calculate()

    def calculate(self):
        """
        Process and stores all the results in self.results
        :return: None
        """
        for tweet in Tweet.objects:
            self.results[tweet.id] = []
            for preference in self.preferences:
                current_value = (len(self.preferences) - (tweet.preferences.index(preference) + 1)) \
                                / (len(self.preferences) - 1)
                self.results[tweet.id].append(current_value)

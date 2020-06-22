import numpy as np

from tweet import Tweet


class PrefToMatrix:

    def __init__(self, preferences):
        """
        This class transforms all the tweets stored in the database
        into a dictionary of preference matrix identified
        by tweet ID.
        :param preferences: the list of the preferences.
        """
        self.preferences = preferences
        self.results = {}
        self.calculate()

    def calculate(self):
        """
        Using the provided formula, calculates the result
        and stores it in self.results
        :return: None
        """
        for tweet in Tweet.objects:
            values = []

            for i in range(len(self.preferences)):
                array = []

                for j in range(len(self.preferences)):
                    current_value = 0

                    if i <= j:
                        current_value = 0.5 * (
                                    1 + (tweet.preferences.index(self.preferences[j]) / len(self.preferences) - 1)
                                    - (tweet.preferences.index(self.preferences[i]) / len(self.preferences) - 1))

                    array.append(current_value)

                values.append(array)

            self.results[tweet.id] = np.array(values)

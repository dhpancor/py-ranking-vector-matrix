from tweet import Tweet


class TopNNormalizer:

    def __init__(self, n_pref):
        """
        TopNNormalizer is a class designed to normalize a
        dataset of tweets.
        :param n_pref: the number of top preferences to be used
        """
        self.n_pref = n_pref
        self.preferences = {}
        self.top_preferences = []
        self.top_n_preferences()

    def top_n_preferences(self):
        """
        Read all the preferences from the users and generates
        a ranked dictionary.
        :return: None
        """
        unsorted_preferences = {}
        for tweet in Tweet.objects:
            for preference in set(tweet.preferences):
                unsorted_preferences[preference] = unsorted_preferences.get(preference, 0) + 1

        self.preferences = {k: v for k, v in
                            sorted(unsorted_preferences.items(), key=lambda item: item[1], reverse=True)}

        self.top_preferences = list(self.preferences.keys())[0:self.n_pref]

    def normalize(self):
        """
        Removes all the unwanted preferences and deletes the tweets
        that doesn't contain at least the TOP N preferences.
        :return: None
        """
        for tweet in Tweet.objects:
            if all(elem in tweet.preferences for elem in self.top_preferences):
                new_preferences = [elem for elem in tweet.preferences if elem in self.top_preferences]
                tweet.preferences = new_preferences
                tweet.save()
            else:
                tweet.delete()

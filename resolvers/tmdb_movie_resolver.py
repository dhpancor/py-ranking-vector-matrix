import requests
import appconfig
from difflib import SequenceMatcher


class TMDBMovieResolver:
    """
    This class is designed to normalize the results of the preferences
    by using the SequenceMatcher algorithm in Python to find similar values.
    For example, "The Irishman" would be also found as "The Irisman" or mistakes
    like that one.

    Specifying a thresold, we can match those two to have the same value,
    and have a more uniform list of preferences.
    """

    def __init__(self, thresold=0.6, year=0):
        """
        Instantiate a new object using TMDBMovieResolver
        :param thresold: the thresold desired for the likelihood
        :param year: of the movies you want to look for
        """
        self.__unique_preferences = []
        self._year = year
        self._thresold = thresold

    @staticmethod
    def __likeliness(a, b):
        """
        Return the likelihood between 0 and 1 of string a and string b
        :param a: first string
        :param b: second string
        :return: the likelihood between them
        """
        return SequenceMatcher(None, a, b).ratio()

    def __get_tmdb_title(self, preference):
        """
        Uses the TMDB API to search for movie titles. The instance _year
        can be specified to make this more accurate.
        :param preference:
        :return: the title of the movie or None if not found
        """
        year_suffix = ('&year=' + str(self._year)) if self._year > 1900 else ''
        url = f'https://api.themoviedb.org/3/search/movie?api_key={appconfig.config["tmdb_api_key"]}{year_suffix}&query={preference}'
        r = requests.get(url)
        if r.status_code == 200:
            response = r.json()
            if response['total_results'] >= 1:
                return response['results'][0]['title']
            else:
                return None

    def process_preference(self, value):
        """
        Checks if there is a preference with a likelihood of equal or greater
        than the specified _thresold from any item in __unique_preferences.

        If not, it will attempt to search the movie in TMDB and add it to the
        __unique_preferences list.

        If not found on TMDB, it will add the value to the __unique_preferences
        :param value: the raw value of the preference
        :return: the normalized value or the same value if not found
        """
        if value not in self.__unique_preferences:
            most_likely_preference = None
            for i in range(len(self.__unique_preferences)):
                if (most_likely_preference is None or
                        self.__likeliness(value, self.__unique_preferences[i]) > self.__likeliness(value, most_likely_preference)):
                    most_likely_preference = self.__unique_preferences[i]

            if most_likely_preference is not None and self.__likeliness(value, most_likely_preference) >= self._thresold:
                return most_likely_preference
            else:
                new_value = self.__get_tmdb_title(value)
                if new_value is not None:
                    self.__unique_preferences.append(new_value)
                return new_value
        else:
            return self.__unique_preferences[self.__unique_preferences.index(value)]

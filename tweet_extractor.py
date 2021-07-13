import csv
import html
import re

from resolvers.tmdb_movie_resolver import TMDBMovieResolver
from schemas.tweet import Tweet


class TweetExtractor:

    regex = r"^[\*\-\d]+[ \.\-]+(.+)$"

    def __init__(self, csv_tweet_file, resolver=TMDBMovieResolver(year=2019)):
        self.csv_tweet_file = csv_tweet_file
        self.raw_tweets = None
        self.__resolver = resolver
        self.extract_tweets_from_csv()

    def extract_tweets_from_csv(self):
        """
        Extract all the tweets found in a CSV file and stores it
        in the raw_tweets instance variable.
        :return: None
        """
        with open(self.csv_tweet_file, 'r', encoding='utf-8') as f:
            self.raw_tweets = list(csv.DictReader(f))

    def __process_matches(self, matches):
        tweet = Tweet()
        for match in matches:
            sanitized_preference = html.unescape(match.group(1).strip())
            sanitized_preference = re.sub(r'[^A-Za-z0-9 ]+', '', sanitized_preference)
            if sanitized_preference is not None and sanitized_preference != "":
                preference_name = self.__resolver.process_preference(sanitized_preference)
                if preference_name is not None:
                    tweet['preferences'].append(preference_name)
                else:
                    raise ValueError
            else:
                raise ValueError
        return tweet

    def process_tweets(self):
        for tweet in self.raw_tweets:
            matches = list(re.finditer(self.regex, tweet['text'], re.MULTILINE))
            if len(set(matches)) > 2:
                try:
                    db_tweet = self.__process_matches(matches)
                    db_tweet.tweet_id = tweet['id']
                    db_tweet.username = tweet['username']
                    db_tweet.created_at = tweet['date']
                    db_tweet.save()
                except:
                    print("Tweet " + tweet['id'] + " not a list or recognized by resolver.")

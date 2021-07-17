import csv
import html
import re
import appconfig

from resolvers.no_resolver import NoResolver
from schemas.tweet import Tweet


class TweetExtractor:

    regex = r"[ ]?[\*\-\d]+[ \.\-]+(.+)"

    def __init__(self, csv_tweet_file, resolver=NoResolver()):
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
            """
            Uncomment the line below for strict preferences. Ignores tilde, and any other character that is not
            a-z A-Z or a number.
            """
            # sanitized_preference = re.sub(r'[^A-Za-z0-9 ]+', '', sanitized_preference)
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

            # When using Twint, it will remove line breaks. This is a workaround for that issue.
            if appconfig.config["using_delimiter"]:
                tweet['tweet'] = tweet['tweet'].replace(appconfig.config["delimiter"], "\n")

            matches = list(re.finditer(self.regex, tweet['tweet'], re.MULTILINE))
            if len(set(matches)) > 2:
                try:
                    db_tweet = self.__process_matches(matches)
                    db_tweet.tweet_id = tweet['id']
                    db_tweet.username = tweet['username']
                    db_tweet.created_at = tweet['date']
                    db_tweet.save()
                except:
                    print("Tweet " + tweet['id'] + " not a list or recognized by resolver.")

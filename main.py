import mongoengine
import appconfig
from TMDBMovieResolver import TMDBMovieResolver
from TweetExtractor import TweetExtractor
from pref_to_matrix import PrefToMatrix
from pref_to_vector import PrefToVector
from top_n_normalizer import TopNNormalizer


if __name__ == '__main__':
    mongoengine.connect(db="twitter_oscars",
                        username=appconfig.config['mongodb']['username'],
                        password=appconfig.config['mongodb']['password'],
                        authentication_source=appconfig.config['mongodb']['authentication_source'],
                        host=appconfig.config['mongodb']['host'])

    # # This process all the tweets found on a CSV using a resolver.
    # tweet_extractor = TweetExtractor('output_got.csv', TMDBMovieResolver(year=2019))
    # tweet_extractor.process_tweets()

    # # This normalizes all the tweets.
    # normalizer = TopNNormalizer(5)
    # normalizer.normalize()

    preferences = [
        'Parasite',
        'Joker',
        'Once Upon a Time… in Hollywood',
        '1917',
        'The Irishman'
    ]

    # vector = PrefToVector(preferences)
    # vector.calculate()

    # matrix = PrefToMatrix(preferences)
    # print(matrix.results['1224890520167747585'])

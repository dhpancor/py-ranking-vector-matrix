import mongoengine
import appconfig
from normalizers.top_n_normalizer import TopNNormalizer
from resolvers.tmdb_movie_resolver import TMDBMovieResolver
from tweet_extractor import TweetExtractor

if __name__ == '__main__':
    mongoengine.connect(db=appconfig.config['mongodb']['db_name'],
                        username=appconfig.config['mongodb']['username'],
                        password=appconfig.config['mongodb']['password'],
                        authentication_source=appconfig.config['mongodb']['authentication_source'],
                        host=appconfig.config['mongodb']['host'])

    # >> STEP1: This process all the tweets found on a CSV using a resolver.
    # tweet_extractor = TweetExtractor('output_got.csv', TMDBMovieResolver(year=2019))
    # tweet_extractor.process_tweets()

    # >> STEP2: This normalizes all the tweets.
    # normalizer = TopNNormalizer(5)
    # normalizer.normalize()

    preferences = [
        'Parasite',
        'Joker',
        'Once Upon a Time… in Hollywood',
        '1917',
        'The Irishman'
    ]

    # >> STEP3-A: Calculate preferences vector.
    # vector = PrefToVector(preferences)
    # vector.calculate()

    # >> STEP3-B: Calculate the preferences matrix.
    # matrix = PrefToMatrix(preferences)
    # print(matrix.results['1224890520167747585'])

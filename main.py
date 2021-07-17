import mongoengine
import appconfig
from normalizers.top_n_normalizer import TopNNormalizer
from resolvers.no_resolver import NoResolver
from resolvers.tmdb_movie_resolver import TMDBMovieResolver
from transformators.pref_to_matrix import PrefToMatrix
from transformators.pref_to_vector import PrefToVector
from tweet_extractor import TweetExtractor

if __name__ == '__main__':
    mongoengine.connect(db=appconfig.config['mongodb']['db_name'],
                        username=appconfig.config['mongodb']['username'],
                        password=appconfig.config['mongodb']['password'],
                        authentication_source=appconfig.config['mongodb']['authentication_source'],
                        host=appconfig.config['mongodb']['host'])

    # >> STEP1: This process all the tweets found on a CSV using a resolver.
    # tweet_extractor = TweetExtractor('prueba2.csv', NoResolver())
    # tweet_extractor.process_tweets()

    # >> STEP2: This normalizes all the tweets.
    # normalizer = TopNNormalizer(4)
    # normalizer.normalize()

    preferences = [
        'Anatomía de Grey',
        'NCIS',
        'Mentes criminales',
        'La que se avecina'
    ]

    # >> STEP3-A: Calculate preferences vector.
    # vector = PrefToVector(preferences)
    # vector.calculate()
    # print(vector.results['1416409686006448129'])

    # >> STEP3-B: Calculate the preferences matrix.
    # matrix = PrefToMatrix(preferences)
    # print(matrix.results['1416409686006448129'])

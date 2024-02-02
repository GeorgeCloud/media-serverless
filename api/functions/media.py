from aws_lambda_powertools.utilities import parameters
import tmdbsimple as tmdb
import json

ssm_provider = parameters.SSMProvider()
tmdb_api_key = ssm_provider.get("/dev/tmdb_api_key", decrypt=True)

tmdb.API_KEY = tmdb_api_key
api_search   = tmdb.Search()

def create_response(data={}, message=None, status=None):
    return {
        "status": status,
        "message": message,
        "data": data
    }

# Complete
def trending_media(event, context):
    return create_response(
        data={
            'trending': tmdb.Trending().info()['results'],
            'movies': tmdb.Discover().movie()['results'],
            'tv_shows': tmdb.Discover().tv()['results'],
        },
        message='success',
        status=200
    )

def popular_movies(event, context):
    movies = tmdb.Movies().popular()['results']
    return create_response(movies, 'success', 200)

def search(event, context):
    path_parameters = event.get('queryStringParameters', {})
    search_query = path_parameters.get('query', {})

    media_results = api_search.multi(query=search_query, include_adult=False)['results']  # includes movies/shows/people

    media_data = []
    for media_result in media_results:
        if 'known_for' in media_result:
            for dict in media_result['known_for']:
                media_data.append(dict)
        else:
            media_data.append(media_result)

    return create_response(media_data, 'success', 200)

def get_media(event, context):
    params = event['queryStringParameters']
    media_type = params.get('media_type')
    media_id = params.get('media_id')

    media = tmdb.Movies(media_id) if 'movie' == media_type else tmdb.TV(media_id)

    media_data = media.info()

    media_trailers = media.videos()['results']
    if media_trailers:
        youtube_key = media_trailers[0]['key']  # Get first youtube key
        media_data.setdefault('youtube_key', youtube_key)

    return create_response(media_data, 'success', 200)

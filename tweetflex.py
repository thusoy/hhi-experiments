from birdy.twitter import UserClient, StreamClient
import os
try: import simplejson as json
except ImportError: import json
import re

CONSUMER_KEY = 'EmwQewB82eqH0uBAObgRp1I4b'
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_TOKEN = '4889176491-6qwuvKfAHgxuQHqOV6Qpl2Axju4OtEaSMiTbd73'
ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

client = StreamClient(CONSUMER_KEY,
                   CONSUMER_SECRET,
                   ACCESS_TOKEN,
                   ACCESS_TOKEN_SECRET)

response = client.stream.statuses.filter.post(track='hhi_cool')

for data in response.stream():
    tweet_text = data['text']
    number = int(re.search(r'\d+', tweet_text).group())
    if number > 1000:
        number = 1000
    print number
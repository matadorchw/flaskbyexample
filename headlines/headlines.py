import feedparser
from flask import Flask, render_template, request
import json
import urllib.request
import urllib.parse

app = Flask(__name__)

RSS_FEEDS = {
    '4sbooks': 'http://www.4sbooks.com/feed',
    'untranslatable': 'https://untranslatable.home.blog/feed/'
}

DEFAULTS = {'publication': '4sbooks',
            'city': 'Shenzhen,CN'}


@app.route('/')
def home():
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)

    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)

    return render_template('home.html', articles=articles, weather=weather)


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=cb932829eacb6a0e9ee4f38bfbf112ed'
    query = urllib.parse.quote(query)
    url = api_url.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {
            'description': parsed['weather'][0]['description'],
            'temperature': parsed['main']['temp'],
            'city': parsed['name']
        }
    return weather


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

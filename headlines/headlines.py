import feedparser
from flask import Flask, render_template, request

app = Flask(__name__)

RSS_FEEDS = {
    '4sbooks': 'http://www.4sbooks.com/feed',
    'untranslatable': 'https://untranslatable.home.blog/feed/'
}


@app.route('/')
def get_news():
    query = request.args.get('publication')
    if not query or query.lower() not in RSS_FEEDS:
        publication = '4sbooks'
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template('home.html', articles=feed['entries'])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

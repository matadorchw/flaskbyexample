import feedparser
from flask import Flask, render_template

app = Flask(__name__)

RSS_FEEDS = {
    'zhihu': 'https://www.zhihu.com/rss',
    'read': 'http://feed.read.org.cn/',
    '163': 'https://news.163.com/special/00011K6L/rss_newsattitude.xml'
}


@app.route('/')
@app.route('/<publication>')
def get_news(publication='163'):
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_article = feed['entries'][0]
    return render_template('home.html', article=first_article)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

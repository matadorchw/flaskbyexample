import feedparser
from flask import Flask

app = Flask(__name__)

RSS_FEEDS = {
    'zhihu': 'https://www.zhihu.com/rss',
    'read': 'http://feed.read.org.cn/',
    '163': 'https://news.163.com/special/00011K6L/rss_newsattitude.xml'
}


@app.route('/')
@app.route('/163')
def news163():
    return get_news('163')


@app.route('/read')
def read():
    return get_news('read')


def get_news(publication):
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_article = feed['entries'][0]
    return '''
<html>
    <body>
        <h1>Headlines</h1>
        <b>{0}</b><br/>
        <i>{1}</i><br/>
        <p>{2}</p><br/>
    </body>
</html>
    '''.format(first_article.get('title'),
               first_article.get('published'),
               first_article.get('summary'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
from feedgen.feed import FeedGenerator
from flask import Flask, make_response, redirect, url_for, render_template, request
from ast import literal_eval
from dateutil import tz
from difflib import SequenceMatcher
from nltk.tokenize import word_tokenize
import requests
import logging
import datetime

BEST_STORIES = 'https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty'
ID_INFO = 'https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'
HN_LINK = 'https://news.ycombinator.com/item?id={}'

app = Flask(__name__, template_folder="./flask/templates/")

def get_news(params):
	articles = list()

	logging.basicConfig(level=logging.DEBUG)
	session = requests.Session()

	stories = literal_eval(session.get(BEST_STORIES).text)
	for story in stories[:params['limit']]:
		article = literal_eval(session.get(ID_INFO.format(str(story))).text)

		if len(params['blacklist']) != 0:
			limit = max([SequenceMatcher(None, forbidden.lower(), article_word.lower()).ratio() 
							for forbidden in params['blacklist']
								for article_word in word_tokenize(article['title'])])
			if limit < params['threshold']:
				articles.append(article)

		else:
			articles.append(article)

	return articles

@app.route('/')
def hello():
	# return redirect(url_for('rss'))
	return render_template('main.html')

@app.route('/rss')
def rss():
	'''
	Reference - https://old.reddit.com/r/flask/comments/evjcc5/question_on_how_to_generate_a_rss_feed/
	'''

	# Default Parameters
	params = {'limit': 5, 
				'blacklist': list(), 
				'threshold': 0.8}

	if 'limit' in request.args:
		params['limit'] = int(request.args.get('limit'))
	if 'nowords' in request.args:
		params['blacklist'] = literal_eval(request.args.get('nowords'))
	if 'similar' in request.args:
		params['blacklist'] = (float(request.args.get('similar')) 
								if float(request.args.get('similar')) <= 1
									else 0.8)

	fg = FeedGenerator()
	fg.title('Hacker News - Best')
	fg.description('Created for personal use by Parth Parikh')
	fg.link(href='https://pncnmnp.github.io')

	UTC = tz.gettz('UTC')

	articles = get_news(params)

	for article in articles:
		fe = fg.add_entry()
		fe.title(article['title'])

		try:
			fe.link(href=article['url'])
		except:
			fe.link(href=HN_LINK.format(str(article['id'])))

		fe.guid(str(article['id']), permalink=False)
		fe.author(name=article['by'])
		fe.published(datetime.datetime.fromtimestamp(article['time'], tz=UTC))

	response = make_response(fg.rss_str())
	response.headers.set('Content-Type', 'application/rss+xml')
	return response
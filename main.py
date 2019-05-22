"""
	Twitter Digest
	Sends a daily Twitter Digest - summary of the previous day's Tweets by a selection
	of Twitter accounts of special interest - to a target user (in this case Jos) by Email.
"""

import tweepy
from datetime import datetime, timedelta
from utils import send_html, record_digest_delivery, digest_delivered_today
import config

if not digest_delivered_today():

	# Authenticate to Twitter API with tweepy
	consumer_key = config.consumer_key
	consumer_secret = config.consumer_secret
	access_token = config.access_token
	access_token_secret = config.access_token_secret

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)


	# Users and the Twitter accounts they'd like to follow - referred to as "digests"
	digests = {
		config.josi_email:  ["ShuhBillSkee", "Livingstone_S", "PrivacyMatters", "futureofprivacy", "MimiTGolden", "WolfieChristl", "johnc1912"],
		config.johannes_email: ["paulg", "nntaleb", "Peter_Dinklage", "DavidDeutschOxf"]
	}

	# Compose and send all "digests"
	for digest_receiver, targets in digests.items():
		
		digest_content = ""
		for each in targets:
			# add name of twitter target to digest
	 		account = api.get_user(each)
			digest_content += "<strong>" + account.name + "</strong>" + "<br>"

			# retrieve last day's tweets 
			tweets = api.user_timeline(screen_name=each, count=100, tweet_mode="extended")

			# separate tweets by kind
			direct_tweets, retweets, responses  = [], [], []
			for tweet in tweets:
				end_date = datetime.now() - timedelta(days=1)
				if not tweet.created_at < end_date:
					tweet_text = tweet.full_text
					if tweet_text.startswith("RT"):
						retweets.append(tweet_text + "<br>")
					elif tweet_text.startswith("@"):
						responses.append(tweet_text + "<br>")
					else:
						direct_tweets.append("- " + tweet_text + "<br>")
				else:
					break

			for each in [direct_tweets, retweets]:
				tweets = "".join(each)
				digest_content += tweets + "<br>"
			digest_content += "<br>" # separator between twitter targets

		digest_content = digest_content.encode('utf-8')
		send_html(digest_receiver, digest_content)
		
	record_digest_delivery()
# Analyse a single tweet
def analyse_tweet(tweet, user_record):
	user_id = tweet['data']['author_id']
	if user_id in user_record:
		user_record[user_id]['tweet_count'] += 1
		print("!!!")
	else:
		user_record[user_id] = {}
		user_record[user_id]['tweet_count'] = 1
gcc = ['1gsyd', '2gmel', '3gbri', '4gade', '5gper', '6ghob', '7gdar', '8acte', '9oter']

# Create dict for sal
def create_sal_dict(sal_data) -> {}:
	sal_dict = {}
	for key in sal_data:
		# Only recording greater capital city
		if sal_data[key]['gcc'][1] in ['g', 'a']:
			sal_dict.update({key: sal_data[key]['gcc']})
	return sal_dict

# Collect data
def combine_gcc_count(gcc_count:[{}]) -> {}:
	res = {'1gsyd': 0, '2gmel': 0, '3gbri': 0, '4gade': 0, '5gper': 0,'6ghob': 0, '7gdar': 0, '8acte': 0, '9oter': 0}
	for i in gcc_count:
		for key, value in i.items():
			res[key] += value 
	return res

def combine_tweet_count(tweet_count, max_rank:int) -> {}:
	# res = {{"123": {'rank':1, 'tweet_count':200}, {}}
	tweet_count = sorted(tweet_count.items(), key=lambda x: x[1]['tweet_count'], reverse=True)
	res = {}
	count = 1
	rank = 0
	for index, user in enumerate(tweet_count):
		if index == 0:
			rank += 1
		else:
			if tweet_count[index-1][1]['tweet_count'] == user[1]['tweet_count']:
				count += 1
			else:
				rank += count
				if rank > max_rank: break
				count = 1
		res[user[0]] = {'rank': rank, 'tweet_count': user[1]['tweet_count']}
	return res

def combine_unique_gcc_count(unique_gcc_count, max_rank:int) -> {}:
	# res = {{"123": {'rank':1, 'res': "6 (#54 tweets - 9gsyd, 9gmel, 9gbri, 9gade, 9gper, 9ghob)"}, {}}
	unique_gcc_count = sorted(unique_gcc_count.items(), key=lambda x: x[1]['res'][0], reverse=True)
	res = {}
	count = 1
	rank = 0
	for index, user in enumerate(unique_gcc_count):
		if index == 0:
			rank += 1
		else:
			if unique_gcc_count[index-1][1]['res'][0] == user[1]['res'][0]:
				count += 1
			else:
				rank += count
				if rank > max_rank: break
				count = 1
		res[user[0]] = {'rank': rank, 'res': user[1]['res']}
	return res

# Sorting
def sort_tweet_count(data:{}, max_rank:int) -> {}:
	data = sorted(data.items(), key=lambda x: x[1]['tweet_count'], reverse=True)
	res = {}
	count = 1
	rank = 0
	for index, user in enumerate(data):
		if index == 0:
			rank += 1
		else:
			if data[index-1][1]['tweet_count'] == user[1]['tweet_count']:
				count += 1
			else:
				rank += count
				if rank > max_rank: break
				count = 1
		res[user[0]] = {'rank': rank, 'tweet_count': user[1]['tweet_count']}
	return res

def sort_unique_gcc_count(data:{}, max_rank:int) -> {}:
	data = sorted(data.items(), key=lambda x: x[1]['unique_city'], reverse=True)
	res = {}
	count = 1
	rank = 0

	for index, user in enumerate(data):
		tweet_count = 0
		gcc_str = ""
		recorded = False
		if index == 0:
			rank += 1
		else:
			if data[index-1][1]['unique_city'] == user[1]['unique_city']:
				count += 1
			else:
				rank += count
				if rank > max_rank: break
				count = 1
		for c in gcc:
			if user[1][c] != 0:
				tweet_count += user[1][c]
				# print(str(user[0]) + " : " + str(user[1][c]) + c[1:])
				if (recorded == True):
					gcc_str += " ,{}{}".format(user[1][c], c[1:])
				else:
					gcc_str = " {}{}".format(user[1][c], c[1:])
				recorded = True

		temp = "{}(#{} tweets -{})".format(data[index][1]['unique_city'], tweet_count, gcc_str)
		res[user[0]] = {'rank': rank, 'res': temp}
	return res

# Print out format
def print_gcc_count(res:{}) -> None:
	print("GCC Ranking")
	print("{:<21} {:<21}".format("Greater Capital City", "Number of Tweets Made"))
	for key, val in res.items():
		print("{:<21} {:<21}".format(key, val))
	return None

def print_tweet_count(res:{}) -> None:
	print("Author Ranking")
	print("{:<5} {:<25} {:<15}".format("Rank", "Author Id", "Number of Tweets Made"))
	for key, val in res.items():
		print("{:<5} {:<25} {:<15}".format(val['rank'], key, val['tweet_count']))
	return None

def print_unique_gcc_count(res:{}) -> None:
	print("Unique GCC Ranking")
	print("{:<5} {:<25} {:<43}".format("Rank", "Author Id", "Number of Unique City Locations and #Tweets"))
	for key, val in res.items():
		print("{:<5} {:<25} {:<43}".format(val['rank'], key, val['res']))
	return None
# Analyse a single tweet
def analyse(req:(str, str), user_record:{}, gcc_count:{}, sal_dict:{}) -> ({}, {}):
	user_id = req[0]
	location = req[1]
	
	# If user has been recorded
	if user_id in user_record:
		user = user_record[user_id]
		user['tweet_count'] += 1
	else:
		user = create_user()
		user_record[user_id] = user
	
	# Handle reading location
	location = read_loc(location, sal_dict)

	# Add a new great capital city
	if len(location) != 0:
		if user[location] == 0:
			user['unique_city'] += 1
		user[location] += 1
		gcc_count[location] += 1
	
	return (user_record, gcc_count)

# Read the location
def read_loc(location:str, sal_dict:{}) -> str:
	gcc = {
		'New South Wales': ('(nsw)', '1gsyd'),
		'Victoria': ('(vic.)', '2gmel'),
		'Queensland': ('(qld)', '3gbri'),
		'South Australia': ('(sa)', '4gade'),
		'Western Australia': ('(wa)', '5gper'),
		'Tasmania': ('(tas.)', '6ghob'),
		'Northern Territory': ('(nt)', '7gdar'),
		'Australian Capital Territory': ('(act)', '8acte'),
		'Great Other Territories': ('(oter)', '9oter')
	}

	city = {
		'Sydney': '1gsyd',
		'Melbourne': '2gmel',
		'Brisbane': '3gbri',
		'Adelaide': '4gade',
		'Perth': '5gper',
		'Tasmania': '6ghob',
		'Darwin': '7gdar',
	}

	loc = location.split(', ')

	if len(loc) < 2:
		location = ""
	elif loc[1] in city:
		location = city[loc[1]]
	elif loc[1] in gcc:
		# check the loc and loc + state
		if loc[0].lower() in sal_dict or loc[0]+" "+gcc[loc[1]][0].lower() in sal_dict:
			location = gcc[loc[1]][1]
		else:
			location = ""
	else:
		location = ""

	return location

# Create new user
def create_user() -> {}:
	user = {
		'tweet_count': 1,
		'unique_city': 0,
		'1gsyd': 0, 
		'2gmel': 0, 
		'3gbri': 0,
		'4gade': 0,
		'5gper': 0,
		'6ghob': 0,
		'7gdar': 0,
		'8acte': 0,
		'9oter': 0,
	}

	return user
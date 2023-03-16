import json

def main():
	print("Let's GO!!!")
	print("\n")

	# Opening JSON file
	f = open('tinyTwitter.json')
	data = json.load(f)
	
	# City dict
	# city_count = {
	# 	'syd': 0, 
	# 	'mel': 0, 
	# 	'bri': 0,
	# 	'ade': 0,
	# 	'per': 0,
	# 	'hob': 0}

	# Iterating through the json
	# list
	for i in data:
		print(i['includes']['places'][0]['full_name'])
	
	# Closing file
	f.close()
	print("\n")
	print("DONE!!!")

if __name__ == "__main__":
    main()
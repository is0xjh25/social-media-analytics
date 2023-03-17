import json
import tweet
import utility

def main():
	print("Let's GO!!!")
	print("\n")

	# Opening JSON file
	tt = open('tinyTwitter.json')
	sal = open('sal.json')

	tt_data = json.load(tt)
	sal_data = json.load(sal)

	sal_dict = utility.create_sal_dict(sal_data)
	# City dict
	gcc_count = {'1gsyd': 0, '2gmel': 0, '3gbri': 0, '4gade': 0, 
				'5gper': 0, '6ghob': 0, '7gdar': 0, '8acte': 0 }

	user_record = {}

	# Iterating through the json
	for i in tt_data:
		# multi-threading...
		tweet.analyse(i, user_record, gcc_count, sal_dict)
	
	# Closing file
	tt.close()
	sal.close()
	print("\n")
	print("DONE!!!")

if __name__ == "__main__":
    main()
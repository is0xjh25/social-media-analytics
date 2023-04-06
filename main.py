import json
import tweet
import utility
import ijson
import sys
from mpi4py import MPI

def main():
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	size = comm.Get_size()
	sal_url = sys.argv[1]
	data_url = sys.argv[2]
	# Load sal.json into dict
	sal_dict = utility.create_sal_dict(json.load(open(sal_url, 'r')))

	if rank == 0:
		master_tweet_processor(comm, sal_dict, data_url)
	else:
		slave_tweet_processor(comm, sal_dict)
	
	return None

def master_tweet_processor(comm, sal_dict, data_url) -> None:
	rank = comm.Get_rank()
	size = comm.Get_size()
	master_work = []
	gcc_count = {'1gsyd': 0, '2gmel': 0, '3gbri': 0, '4gade': 0, '5gper': 0,'6ghob': 0, '7gdar': 0, '8acte': 0, '9oter': 0}
	user_record = {}

	# Read fiel object by object
	with open(data_url, 'rb') as f:
		for record in ijson.items(f, 'item', multiple_values=True):
			user_id = record['data']['author_id']
			location = record['includes']['places'][0]['full_name']
			divide = 0
			if size == 1:
				user_record, gcc_count = tweet.analyse((user_id, location), user_record, gcc_count, sal_dict)
			else:
				# Assign task into different nodes based on the last numeber of user_id
				if (user_id[-1].isdigit()):
					divide = int(user_id[-1])%size
				else:
					divide = ord(user_id[-1])%size
				if divide == 0:
					master_work.append((user_id, location))
				else:
					req = comm.send((user_id, location), dest=divide, tag=divide)
	# Master's own task
	for index, t in enumerate(master_work):
		user_record, gcc_count = tweet.analyse(t, user_record, gcc_count, sal_dict)
	# Result from the master
	task_1 = gcc_count
	task_2 = utility.sort_tweet_count(user_record, 10)
	task_3 = utility.sort_unique_gcc_count(user_record, 10)
	# Collect and summerise the result from the slaves
	if size > 1:
		res = marshall_tweets(comm, task_1, task_2, task_3)
		task_1 = res['task_1']
		task_2 = res['task_2']
		task_3 = res['task_3']
		# Close all the slaves
		for i in range(size-1):
			comm.send('exit', dest=(i+1), tag=(i+1))
	# Print out the results
	print("\n")
	utility.print_gcc_count(task_1)
	print("\n")
	utility.print_tweet_count(task_2)
	print("\n")
	utility.print_unique_gcc_count(task_3)
	print("\n")
	return None

def slave_tweet_processor(comm, sal_dict):
	rank = comm.Get_rank()
	size = comm.Get_size()
	gcc_count = {'1gsyd': 0, '2gmel': 0, '3gbri': 0, '4gade': 0, '5gper': 0,'6ghob': 0, '7gdar': 0, '8acte': 0, '9oter': 0}
	user_record = {}

	while True:
		in_comm = comm.recv(source=0, tag=rank)
		if isinstance(in_comm, tuple):
			# Receive task from the master
			user_record, gcc_count = tweet.analyse(in_comm, user_record, gcc_count, sal_dict)
		elif isinstance(in_comm, str):
			if in_comm in ("return_data"):
				comm.send({'gcc_count': gcc_count, 'tweet_count': utility.sort_tweet_count(user_record, 10), 'unique_gcc_count': utility.sort_unique_gcc_count(user_record, 10)}, dest=0, tag=0)
			elif in_comm in ("exit"):
				exit(0)

def marshall_tweets(comm, master_gcc_count, master_tweet_count, master_unique_gcc_count) -> ({}, {}, {}):
	processes = comm.Get_size()
	total_gcc_count = [master_gcc_count]
	total_tweet_count = master_tweet_count
	total_unique_gcc_count = master_unique_gcc_count

	for i in range(processes-1):
		comm.send('return_data', dest=(i+1), tag=(i+1))
	for i in range(processes-1):
		temp = (comm.recv(source=(i+1), tag=0))
		total_gcc_count.append(temp['gcc_count'])
		total_tweet_count.update(temp['tweet_count'])
		total_unique_gcc_count.update(temp['unique_gcc_count'])
	
	# The final results
	final_gcc_count = utility.combine_gcc_count(total_gcc_count)
	final_tweet_count = utility.combine_tweet_count(total_tweet_count, 10)
	final_unique_gcc_count = utility.combine_unique_gcc_count(total_unique_gcc_count, 10)

	return {'task_1': final_gcc_count, 'task_2': final_tweet_count, 'task_3': final_unique_gcc_count}

if __name__ == "__main__":
    main()
import json
import tweet
import utility
from mpi4py import MPI

def main():
	# Opening JSON file
	data = json.load(open('tinyTwitter.json', 'r'))
	sal_dict = utility.create_sal_dict(json.load(open('sal.json', 'r')))

	# City dict
	gcc_count = {'1gsyd': 0, '2gmel': 0, '3gbri': 0, '4gade': 0, '5gper': 0, 
				'6ghob': 0, '7gdar': 0, '8acte': 0, '9oter': 0}
	user_record = {}

	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	
	if rank == 0:
		master_tweet_processor(comm, data, user_record, gcc_count, sal_dict)
	else:
		slave_tweet_processor(comm, data, user_record, gcc_count, sal_dict)
	
	# 分散data (MASTER)
	# 處理data (SLAVE)
	# 回收數據
	# 整合 user_record, gcc_count (MASTER - combine_gcc_count(), combine_user_record())
	# 分散 user_record (MASTER)
	# 處理排序 (SLAVE) (need a new function)
	# print out (MASTER)

	# utility.print_gcc_count(gcc_count)
	# print("\n")
	# utility.print_author_count(utility.sort_author_count(user_record, 10))
	# print("\n")
	# utility.print_unique_gcc_count(utility.sort_unique_gcc_count(user_record, 10))
	return None

def master_tweet_processor(comm, data, user_record, gcc_count, sal_dict) -> None:
    rank = comm.Get_rank()
    size = comm.Get_size()
	# 怎么split 在各自的slave處理？？？
	# data = data.split()
	# master 处理自己的那一份

    result = tweet.analyse(data[0], user_record, gcc_count, sal_dict)
    for i in range(1, size):
	    req = comm.send(data[i], dest=i, tag=0)
    
    return None
	
def slave_tweet_processor(comm, data, user_record, gcc_count, sal_dict):
	rank = comm.Get_rank()
	size = comm.Get_size()

	result = analyze(data, user_record, gcc_count, sal_dict)
	# Now that we have our counts then wait to see when we return them.
	while True:
		in_comm = comm.recv(source=MASTER_RANK, tag=rank)
		# Check if command
		if isinstance(in_comm, str):
			if in_comm in ("return_data"):
				# print("Process: ", rank, " sending back ", len(counts), " items")
				comm.send(result, dest=MASTER_RANK, tag=MASTER_RANK)
			elif in_comm in ("exit"):
				exit(0)
	
if __name__ == "__main__":
    main()
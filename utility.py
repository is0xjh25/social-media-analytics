# Create dict for sal
def create_sal_dict(sal_data) -> {}:
	sal_dict = {}
	for key in sal_data:
		# Only recording greater capital city
		if sal_data[key]['gcc'][1] in ['g', 'a']:
			sal_dict.update({key: sal_data[key]['gcc']})
	return sal_dict
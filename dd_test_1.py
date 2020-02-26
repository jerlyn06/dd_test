'''script to detail image sequences in a folder and list their count '''

import os,re

fpath = r"E:\Python\dd_test\test1" # folder path

def lss(fpath):
	'''function to return summary of image sequence files in folder
	fpath (string) - valid folder path accessible on the local drive
	'''
	contents = [f for f in os.listdir(fpath)] # list all files in folder
	file_exts = set([os.path.splitext(file)[-1] for file in contents]) # retrieve unique extensions

	f_update = {} # dictionary to group files and information as key-value pairs with extension as keys
	indices = []
	for ext in file_exts:
		files = [f for f in contents if f.endswith(ext)] # get files matching extensions
		num_place = re.compile(r"(\d+)")
		for f in files:
			nums = num_place.findall(f) # only returns numbers in a string
			if num_place:
				idx = [f.find(x) for x in nums] # get indices of numbers in string
				temp = {f: {'nums': nums, 'idx': tuple(idx)}} # dictionary returns all the numbers and their indices
				indices.append(tuple(idx))
				f_update.update(temp)
	# print(f_update)

	# group and modify dictionary by index positions where the numbers occur. We do this to check if there are any missing frames in the image sequence
	for i in set(indices):
		# print(i)
		get_files = [k for k, v in f_update.items() if v['idx'] == i] # files matching index positions
		nums = [v['nums'] for k,v in f_update.items() if v['idx']==i] # frames in file names
		# update dictionary to remove individual files as keys and replace them with group of files
		for f in get_files:
			f_update.pop(f,None)
		f_update.update({tuple(get_files):{'nums':nums,'idx':i}})

	print(f_update,'up')

	# group by frame numbers pending difference
	summary_dict = {}
	for k,v in f_update.items():
		frames_list = v['nums']
		frames_check = [x for num in frames_list for x in num] # join list of lists to single int list

		if all(len(i)==len(frames_check[0]) for i in frames_check): # check if any number in filename is the frame padding by comparing the length of frames
			int_frames = [int(x) for x in frames_check] # convert str to int to check if the frames are in ascending order and identify missing frames
			int_frames.sort()
			try:
				seq_frames = [x for x in range(int_frames[0],int_frames[-1]+1)]
				if len(seq_frames) == len(int_frames):
					# files to replace the frame numbers in the print style specified
					files = [y.replace(i,"%0{0}d".format(str(len(i)))) for i in frames_check for y in k]
					if len(files)>1:
						summary_dict.update({tuple(files):{'frames':seq_frames}})
					else: # for single files with number
						summary_dict.update({k:{'frames':[]}})

				else:
					missing_frames = sorted(list(set(seq_frames) - set(int_frames)))


			except IndexError:
				# for filenames that are only text
				summary_dict.update({k: {'frames': []}})

		else:
			# check file pattern by comparing if number is in filename
			for i in range(len(frames_list)):
				if frames_list[i][0] in k[0]:
					files = [f for f in k if frames_list[i][0] in f]
					rem_files = 12
			print(files,'files')

	return summary_dict



folder_summary = lss(fpath)
# -*- coding:utf-8 -*-
#将指定文件夹下的文件按数量切分支新文件夹下

import os
import sys
import shutil


class DirSplite(object):
	def __init__(self, root, dst_root):
		self.m_root = root
		self.m_dst_root = dst_root

	def splite(self, once):
		if os.path.exists(self.m_root) is False:
			raise SystemExit("[Error] path is not exist")
		for root, dirs, files in os.walk(self.m_root):
			file_len = len(files)
			times = int(file_len / once) + 1
			for i in range(times):
				tmp = (i + 1) * once
				count = tmp
				if tmp > file_len:
					count = file_len
				for index in range(i * once, count):
					# print(index, count, i)
					dst_path = os.path.join(self.m_dst_root, str(i))
					if os.path.exists(dst_path) is False:
						os.makedirs(dst_path)
					file = files[index]
					shutil.copy(os.path.join(root, file), os.path.join(dst_path, file))
					print("time: {0}, index: {1}".format(i, index))


if __name__ == "__main__":
	argv = sys.argv
	print(str(argv))
	argv_len = len(argv)
	if argv_len != 4:
		raise SystemExit("[Params Error] first param: source file dir, second param: object file dir, third param: splite count\nexample: python image_splite.py ./file/person ./obj/person_part_200 200")
	if os.path.exists(argv[2]) is False:
		os.makedirs(argv[2])
	spliter = DirSplite(argv[1], argv[2])
	spliter.splite(int(argv[3]))
	print("finish")

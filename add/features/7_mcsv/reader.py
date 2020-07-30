#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gzip
from enum import Enum



VOL = "/home/nia/Development/_Python/_DCat/ExportA/Video.sson.gz"

DET = "-"*10

class Sections(Enum):
	header = 0
	body = 1


def __ukv(line: str) -> list:
	return line.split("|")


def __read_header(fd):
	header = {}
	det = "-"*10
	r = False
	c = 20
	while not r:
		line = fd.readline().strip()
		# print(line)
		print(line)
		
		
		
		if line == det:
			print("det!!")
			break
			
			
		try:
			key, value, *_ = __ukv(line)
			header[key] = value
		except Exception as e:
			print(e)

		c -=1
		if c<0:
			break
			
	print(header)




def main():
	fd = gzip.open(VOL, "rt", encoding="utf-8")
	
	# __read_header(fd)

	sheader = []
	sbody = []
	
	section = Sections.header
	c = 1000
	while True:
		
		line = fd.readline().strip()
		if not line:
			print("null line")
			break
		
		if section == Sections.header:
			if line == DET:
				section = Sections.body
			else:
				sheader.append(line)
		elif section == Sections.body:
			sbody.append(line)
		else:
			pass
	
	
	
	
		c -= 1
		if c < 0:
			print("emerg")
			break
	
	
	fd.close()
	
	print("len header:", len(sheader))
	print("len body:", len(sbody))
	




if __name__ == "__main__":
	main()

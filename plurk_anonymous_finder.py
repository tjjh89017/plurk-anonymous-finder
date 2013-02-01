#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib2


def get_user_id(url):
	
	if not url:
		return -1
	
	req = urllib2.urlopen(url, timeout = 80)
	if not req:
		return -2

	pattern = re.compile('^.*"user_id": (\d+),.*$', re.S)
	rawdata = req.read()
	if not rawdata:
		return -3

	match = pattern.match(rawdata)
	if match:
		return int(match.group(1), 10)

	return -4


def get_friend_list_from_id(id):

	URL = "http://www.plurk.com/Friends/showFriendsBasic?user_id=%d&offset=%d"
	pattern = re.compile('<li> <a href="(http://www.plurk.com/\w+)" target="_top">', re.S)
	friend_list = []

	if not id:
		return [];

	offset = 0;
	while True:
		req = urllib2.urlopen(URL % (id, offset), timeout = 80)
		if not req:
			break;
		rawdata = req.read()
		find = pattern.findall(rawdata)
		if not find:
			break;
		friend_list += find
		offset += 10
	
	return friend_list


def find_possible(list):

	friend_table = {}

	for user in list:
		id = get_user_id(user)
		friend_list = get_friend_list_from_id(id)
		friend_list.append(user)

		for friend in friend_list:
			if not friend in friend_table:
				friend_table[friend] = 0
			friend_table[friend] += 1

	friend_table["http://www.plurk.com/plurkbuddy"] = 0
	max = 0
	for possible in friend_table.keys():
		if friend_table[possible] > max:
			max = friend_table[possible]

	possible_list = []
	for possible in friend_table.keys():
		if friend_table[possible] == max:
			possible_list.append(possible)

	return possible_list

if __name__ == "__main__":

	response_list = []

	result = find_possible(list)
	for friend in result:
		print friend

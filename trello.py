#!/usr/bin/env python

import sys; sys.path.insert(0, "/usr/local/lib/python2.7/site-packages")
from trello import TrelloClient
import os
import datetime
import textwrap
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--board", help='board to print (defaults to "A&O")', default="A&O")
parser.add_argument("-l", "--label", help='filter by label (defaults to none)')
args = parser.parse_args()


print "From: Alexander Graf <agraf@suse.de>"
print "Subject: A&O Week %02d, Alex" % ( datetime.datetime.now().isocalendar()[1] )
print ""

trello = TrelloClient("3056bae48f861018da6448a23b704258", "83b7dcd81038245d9cc02aff8d085c55e4bae38de0eb32f7297cb41060608a6f")

boards = trello.list_boards()

def split_len(seq, length):
	return [seq[i:i+length] for i in range(0, len(seq), length)]

def print_item(indent, text):
	separator = '-'
	for line in textwrap.wrap(text, 80 - 7):
		print "%s%s %s" % ( indent, separator, line )
		separator = ' '

def may_print_card(c):
	if len(c.labels) == 0:
		return 1
	if args.label == None:
		return 1
	for l in c.labels:
		if l["name"] == args.label:
			return 1
	return 0

def checkx(c):
	if c['checked']:
		return 'X'
	return ' '

for b in boards:
	if b.name != args.board:
		continue
	for l in b.all_lists():
		cards = l.list_cards()
		print_list = 0
		for c in cards:
			c.fetch()
			if (may_print_card(c) == 0):
				continue
			print_list = 1
		if print_list == 0:
			continue
		print ""
		print "[%s]" % ( l.name )
		for c in cards:
			if (may_print_card(c) == 0):
				continue
			print_item("  ", c.name)
			if len(c.checklists) > 0:
				for cl in c.checklists:
					for i in cl.items:
						print_item("    ", "[%s] %s" % ( checkx(i), i['name'] ))
			for co in reversed(c.comments):
				print_item("    ", co['data']['text'])
	break

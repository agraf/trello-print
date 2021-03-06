#!/usr/bin/env python

import sys; sys.path.insert(0, "/usr/local/lib/python2.7/site-packages")
from trello import TrelloClient
from operator import itemgetter
import os
import datetime
import textwrap
import argparse
import bugzilla
from bugzilla import Bugzilla
import logging


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

def check_bugzilla(url):
	global bz

	if not url.startswith("https://bugzilla.novell.com"):
		return
	try:
		if bz == None:
			bz = Bugzilla(url="https://bugzilla.novell.com/xmlrpc.cgi", cookiefile=None)
		bug_id = url[url.find("id=")+3::]
		bug = bz._getbug(int(bug_id))
		bug_desc = bug['short_desc']
	except Exception as e:
		bug_desc = e
	print_item(4*" ", "(%s)" % bug_desc)

def labels(card):
	if args.printlabels == False:
		return ""
	r = ""
	for l in c.labels:
		r += "[%s] " % l["name"]
	return r

###############################################################################

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--board", help='board to print (defaults to "A&O")', default="A&O")
parser.add_argument("-l", "--label", help='filter by label (defaults to none)')
parser.add_argument("--printlabels", help='print labels (defaults to false)', action="store_true")
parser.add_argument("-L", "--listboards", help='list all available boards', action="store_true")
parser.add_argument("-u", "--devkey", help='developer key to access trello', required=True)
parser.add_argument("-p", "--secret", help='developer secret to access trello', required=True)
args = parser.parse_args()

trello = TrelloClient(args.devkey, args.secret)
boards = trello.list_boards()
bz = None

if args.listboards:
	boards = trello.list_boards()
	for b in boards:
		print b.name
	sys.exit()

for b in boards:
	if b.name != args.board:
		continue
	firstlist = True
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
		if firstlist == True:
			firstlist = False
		else:
			print ""
		print "[%s]" % ( l.name )
		for c in cards:
			if (may_print_card(c) == 0):
				continue
			print_item(2*" ", "%s%s" % ( labels(c), c.name ) )
			check_bugzilla(c.name)
			if len(c.checklists) > 0:
				for cl in c.checklists:
					for i in sorted(cl.items, key=itemgetter('pos')):
						print_item(4*" ", "[%s] %s" % ( checkx(i), i['name'] ))
			for co in reversed(c.comments):
				print_item(4*" ", co['data']['text'])
	break

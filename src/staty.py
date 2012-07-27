#! /usr/bin/env python

import twitter
import sys
import os.path
import ConfigParser
from subprocess import *

Usage = """
Use ./staty.py [options]
"""

description = """
Staty is a full fledged twitter client


       -------------------------------------------------------
      ____   _________        __          __________
     /  __| |___  ____|      // \\       |___  _____| \\     //
    /  /        | |         //__ \\          | |       \\   //
    \  \__      | |        //____ \\         | |        \\_//
     \__  \     | |       //       \\        | |         | |
      __/ /     | |      //         \\       | |         | |
     |___/      |_|     //           \\      |_|         |_|

   =============================================================
   Tweets options:

   tweet
   friends
   system
   msg
   followers
   vc
   replies
   feed
   quote

"""

check = os.path.isfile(os.path.expanduser('~/.staty.conf'))
if cmp(check,False) == 0:
    print "Run the ./install.sh and check again!"
    sys.exit(2)


config = ConfigParser.ConfigParser()
config.read(os.path.expanduser('~/.staty.conf'))
conskey = config.get("STATY","consumer_key",raw=True)
conssec = config.get("STATY","consumer_secret",raw=True)
accstkn = config.get("STATY","access_token",raw=True)
accssec = config.get("STATY","access_token_secret",raw=True)

api = twitter.Api(consumer_key=conskey,consumer_secret=conssec,access_token_key=accstkn,access_token_secret=accssec)

if len(sys.argv) == 1:
	print description
	print '\n'
	print Usage
	sys.exit(2)

if (cmp(sys.argv[1],'-h') or cmp(sys.argv[1],'--help')) == 0:
	print Usage
	sys.exit(2)

if cmp(sys.argv[1],"friends") == 0:
        users = api.GetFriends()
        print "\n".join([u.name for u in users])

if cmp(sys.argv[1],"msg") == 0:
        msg = api.GetDirectMessages()
        print "\n".join([u.text for u in msg])

if cmp(sys.argv[1],"followers") == 0:
        followers = api.GetFollowers()
        print "\n".join([u.name for u in followers])

if cmp(sys.argv[1],"vc") == 0:
        vc = api.VerifyCredentials()
        print vc

if cmp(sys.argv[1],"replies") == 0:
        reply = api.GetReplies()
        print [u.text for u in reply]

if cmp(sys.argv[1],"update") == 0 or cmp(sys.argv[1],"tweet") == 0:
	status=' '.join(sys.argv[2:])
	if len(status) < 140:
		api.PostUpdates(status)
		print "Status Is Updated Successfully!"
	else:
		print "Your status is of "+str(len(status))+"chars.Twitter doesn't allow more than 140 chars"

if cmp(sys.argv[1],"feed") == 0 and len(sys.argv) == 4:
	feeds=api.GetUserTimeline(sys.argv[2],count=sys.argv[3])
	print "\n".join([feed.text for feed in feeds])

if cmp(sys.argv[1],"search") == 0:
	search = api.GetSearch(' '.join(sys.argv[2:]))
	print [getattr(s.user,"screen_name")+":"+getattr(s,"text") for s in search]


if cmp(sys.argv[1],"system") == 0:
    stuff = Popen(["./sysinfo.sh"],stdout=PIPE)
    link = Popen(["pastebinit"],stdin=stuff.stdout,stdout=PIPE)
    status = link.communicate()[0]
    api.PostUpdates(status)

if cmp(sys.argv[1],"quote") == 0:
    status = Popen(["./quote.sh"],stdout=PIPE).communicate()[0]
    api.PostUpdates(status)




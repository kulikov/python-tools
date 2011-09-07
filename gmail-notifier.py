#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import urllib2, os
import feedparser
from pyxmpp2.simple import send_message
from pyxmpp2.settings import XMPPSettings
from optparse import OptionParser


def sendJabberMessage(text, opts):
    send_message(source_jid=opts.botJid, password=opts.botPass,
                 target_jid=opts.targetJid, 
                 body=text,
                 settings=XMPPSettings({"starttls": True, "tls_verify_peer": False, "server": 'talk.google.com', "port": 5222}))



if __name__ == "__main__":


    optp = OptionParser()

    optp.add_option("-a", "--auth", dest="auth", help="GMail http basic auth hash")
    optp.add_option("-b", "--botjid", dest="botJid", help="bot's jabber id")
    optp.add_option("-p", "--botpass", dest="botPass", help="bot's jabber password")
    optp.add_option("-t", "--targetjid", dest="targetJid", help="message recepient jid")

    opts, args = optp.parse_args()


    request = urllib2.Request("https://mail.google.com/mail/feed/atom")
    request.add_header("Authorization", "Basic " + opts.auth)
    result = urllib2.urlopen(request)

    rss = feedparser.parse(result.read())

    if (len(rss['entries']) > 0):

        f = open(os.path.dirname(__file__) + '/msgs.list', 'r+a')
        seens = f.read().split("\n")

        for item in rss['entries']:
            if (item['id'] not in seens):
                sendJabberMessage("*%s* \n%s\n\n%s" % (item['title'], item['author'], item['summary']), opts)
                f.write(item['id'] + "\n")
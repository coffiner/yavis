#!/usr/bin/python

import sys
import urllib2

response = urllib2.urlopen(sys.argv[1])
html = response.read()

print html

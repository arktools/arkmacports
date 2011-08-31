#!/usr/bin/python

import urllib
name = "euler"
url = "http://github.com/lennax/euler/tarball/v0.3"
print "Downloading file '%s'" % name
urllib.urlretrieve(url, name + ".tar.gz")
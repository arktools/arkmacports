#!/usr/bin/python

import sys
import os
import subprocess

#print "argv[0]: " + sys.argv[0]
#print "getcwd: " + os.getcwd()
path = os.path.abspath(__file__)
#print "__file__ path: " + path
script_dir = os.path.dirname(os.path.abspath(__file__))
#print "base: " + script_dir
# subprocess.check_call(["touch", "CWDTEST"])
call_dir = os.getcwd()
#tree = os.walk(call_dir)
#for root, dirs, files in os.walk(call_dir):
	#for name in files: 
	#for name in dirs:
	
#for i in tree: 
	#print i
	#break

build_dir=""
script_mom = os.path.abspath(script_dir+"/..")
script_grandma = os.path.abspath(script_mom+"/..")
if script_mom == call_dir:
	script_mom = ""
if script_grandma == call_dir:
	script_grandma = ""
# print "mom: %s" % script_mom
# print "grandma: %s" % script_grandma

def find_build_dir(search_dir):
#	buildfile = "CMakeLists.txt"
#	srcdir = "src"
	buildfile = "BUILDFILE"
	srcdir = "BUILDDIR"
	os.chdir(search_dir)
	if os.path.isfile(buildfile) and os.path.isdir(srcdir):
		print "buildfile and srcdir found in '%s'" % search_dir
		build_dir = search_dir
		return build_dir
	return False

# Class to emulate if temp = x (checking equality of x while assigning it to temp)
# Borrowed from Alex Martelli
class Holder(object):
	def set(self, value):
		self.value = value
		return value
	def get(self):
		return self.value

temp = Holder()


if temp.set(find_build_dir(call_dir)): 
	build_dir = temp.get()
elif temp.set(find_build_dir(script_dir)): 
	build_dir = temp.get()
elif script_mom and temp.set(find_build_dir(script_mom)): 
	build_dir = temp.get()
elif script_grandma and temp.set(find_build_dir(script_grandma)):
	build_dir = temp.get()
else: 
	print "Could not find a valid build directory"

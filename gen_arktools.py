#!/usr/bin/python
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Author: Lenna X. Peterson (github.com/lennax)

# TODO: 
# Split settings into separate file
# Allow specification of phase options
# Parse version numbers, pull by tag

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import os
import subprocess
import urllib
from string import Template

# SETTINGS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
## Port development paths ##
LOCAL_PORT_TREE = "~/ports"
PORTFILE_PATH = "Portfile" # relative to this script

## Project settings ##
GIT_PATH = "arktools"
HOMEPAGE = "http://arktools.github.com"
# Replace with something accurate later
VERSION = "0.0.0"
CATEGORY = "science"
PLATFORM = "darwin"
LICENSE = "GPL-3"
MAINTAINERS = "gmail.com:arklenna \\\n                  gmail.com:james.goppert"
BUILD = "cmake"

## Project member settings ##
ports = {
	'arkcomm': {
		'DEPS': [
#			"mavlink",
		],
		'DESCRIPT': "Autonomous Robotics Kit communications library",
		'LONG_DESCR': "ark (Autonomous Robotics Kit) Communications Library",
	},
	'arkmath': {
		'DEPS': [
		],
		'DESCRIPT': "Autonomous Robotics Kit math library",
		'LONG_DESCR': "ark (Autonomous Robotics Kit) Math Library",
	},
	'arkosg': {
		'DEPS': [
			"boost",
			"qt4-mac-devel",
			"OpenSceneGraph",
		],
		'DESCRIPT': "Autonomous Robotics Kit, OpenSceneGraph library",
		'LONG_DESCR': "ark (Autonomous Robotics Kit), OpenSceneGraph library",
	},
	'arkscicos': {
		'DEPS': [
			"arkcomm",
			"arkmath",
			"arkosg",
		],
		'DESCRIPT': "Autonomous Robotics Kit, Scicoslab toolbox",
		'LONG_DESCR': "ark (Autonomous Robotics Kit), Scicoslab Toolbox",
	},
}

# MAIN PROGRAM # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
## Store paths
port_path = os.path.expanduser(LOCAL_PORT_TREE)
base_path = os.getcwd()
template_path = os.path.join(base_path, PORTFILE_PATH)

for k in ports.keys():
	print "Project '%s'" % k
	
	## Determine dependencies
	dep_str = ""
	if len(ports[k]['DEPS']) > 0:
		for i, d in enumerate(ports[k]['DEPS']):
			dep_str += "port:"+d.rstrip() 		# whitespace causes failure
			if i < len(ports[k]['DEPS'])-1: 
				dep_str += " \\\n                  " # 18 spaces
		print "deps: %s" % dep_str
	
	## [Clone and] update source
	if os.path.exists(k) == False:
		print "Cloning project '%s'..." % k
		git_file = "git@github.com:%s/%s.git" % (GIT_PATH, k)
		subprocess.check_call(["git", "clone", git_file])
	os.chdir(k)
	### Update source
	subprocess.check_call(["git", "pull"])
	### Get commit ID
	unique = subprocess.Popen(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE).communicate()[0]
	short_unique = unique[0:7]
	commit = unique.rstrip()
	
	## Determine checksums
	### Download file
	url = "http://github.com/%s/%s/tarball/%s" % ( GIT_PATH, k, commit )
	barefile = "%s-%s-%s.tar.gz" % ( GIT_PATH, k, short_unique )
	filename = os.path.join( base_path, barefile )
	if os.path.exists(filename) == False:
		urllib.urlretrieve(url, filename)
	### Calculate checksums
	md5_str = subprocess.Popen(["md5", filename], stdout=subprocess.PIPE).communicate()[0]
	md5 = md5_str.rstrip().split(' ')[-1]
	sha1_str = subprocess.Popen(["openssl", "sha1", filename], stdout=subprocess.PIPE).communicate()[0]
	sha1 = sha1_str.rstrip().split(' ')[-1]
	rmd160_str = subprocess.Popen(["openssl", "rmd160", filename], stdout=subprocess.PIPE).communicate()[0]
	rmd160 = rmd160_str.rstrip().split(' ')[-1]
	
	## Create Portfile
	### Create dict for Portfile Template
	d = dict(
		portname = k,
		version = VERSION, 
		category = CATEGORY,
		platform = PLATFORM, 
		lic = LICENSE, 
		maint = MAINTAINERS, 
		descript = ports[k]['DESCRIPT'], 
		long_descr = ports[k]['LONG_DESCR'], 
		homepage = HOMEPAGE,
		build_depends = "port:"+BUILD, 
		lib_depends = dep_str,
		master_site = url,
		filename = "%s-${name}-%s" % (GIT_PATH, short_unique),
		md5 = md5, 
		sha1 = sha1, 
		rmd160 = rmd160
	)
	### Substitute dict into Template, write Portfile

	f = open(template_path)
	out = open("Portfile", 'w')
	sub = Template(f.read()).safe_substitute(d)
	f.close()
	out.write(sub)
	out.close()
	
	## Copy Portfile to local port tree
	copy_path = os.path.join( port_path, CATEGORY, k )
	print copy_path
	if os.path.exists(copy_path) == False:
		subprocess.check_call(["mkdir", copy_path])
	subprocess.check_call(["mv", "Portfile", copy_path])
	
	## Return to original directory
	os.chdir(base_path)

## Run portindex to verify Portfile syntax
os.chdir(port_path)
subprocess.check_call(["portindex"])

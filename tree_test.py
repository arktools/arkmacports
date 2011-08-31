#!/usr/bin/python

ports = {
	'arkcomm': {
		'deps': [
			"mavlink"
		],
		'descript': "Autonomous Robotics Kit communications library",
		'long_descr': "ark (Autonomous Robotics Kit) Communications Library",
	},
	'arkmath': {
		'deps': [
		],
		'descript': "Autonomous Robotics Kit math library",
		'long_descr': "ark (Autonomous Robotics Kit) Math Library",
	},
	'arkosg': {
		'deps': [
			"boost",
			"qt-4-mac",
			"OpenSceneGraph-devel"
		],
		'descript': "Autonomous Robotics Kit, OpenSceneGraph library",
		'long_descr': "ark (Autonomous Robotics Kit), OpenSceneGraph library",
	},
	'arkscicos': {
		'deps': [
			"arkcomm",
			"arkmath",
			"arkosg"
		],
		'descript': "Autonomous Robotics Kit, Scicoslab toolbox",
		'long_descr': "ark (Autonomous Robotics Kit), Scicoslab Toolbox",
	},
}

git_path = "arktools"
homepage = "http://arktools.github.com"

import os
import subprocess
import urllib
from string import Template

#print ports['mavlink']['long_descr']
for k in ports.keys():
	if ports[k]['git_path'] == "":
		git_path = "arktools"
	else: 
		git_path = ports[k]['git_path']
	print "Project '%s'" % k
	if os.path.exists(k) == False:
		print "Cloning project '%s':" % k
		cmd = "git clone git@github.com:%s/%s.git" % (git_path, k)
		print cmd
		subprocess.check_call(cmd, shell=True)
	os.chdir(k)
#	subprocess.check_call(["git", "pull"])
	unique = subprocess.Popen(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE).communicate()[0]
	print unique.rstrip()
	short_unique = unique[0:7]
	print short_unique
	
	dep_str = ""
	if len(ports[k]['deps']) > 0:
		for i, d in enumerate(ports[k]['deps']):
			dep_str += "port:"+d
			if i < len(ports[k]['deps'])-1: 
				dep_str += " \ \n    "
		print "deps: %s" % dep_str
	
	commit = unique.rstrip()
	url = "http://github.com/%s/%s/tarball/%s" % ( git_path, k, commit )
	filename = "../%s-%s-%s.tar.gz" % (git_path, k, short_unique)
	if os.path.exists(filename) == False:
		urllib.urlretrieve(url, filename)
	md5_str = subprocess.Popen(["md5", filename], stdout=subprocess.PIPE).communicate()[0]
	md5 = md5_str.rstrip().split(' ')[-1]
	sha1_str = subprocess.Popen(["openssl", "sha1", filename], stdout=subprocess.PIPE).communicate()[0]
	sha1 = sha1_str.rstrip().split(' ')[-1]
	rmd160_str = subprocess.Popen(["openssl", "rmd160", filename], stdout=subprocess.PIPE).communicate()[0]
	rmd160 = rmd160_str.rstrip().split(' ')[-1]
	
	version = "0.0.0"
	if ports[k]['homepage'] == "": 
		homepage = "http://arktools.github.com"
	else: 
		homepage = ports[k]['homepage']
	filename = "%s-${name}-%s" % (git_path, short_unique)
	
	d = dict(
		name = k,
		version = version, 
		descript = ports[k]['descript'], 
		long_descr = ports[k]['long_descr'], 
		homepage = homepage,
		depends = dep_str,
		master_site = url,
		filename = filename,
		md5 = md5, 
		sha1 = sha1, 
		rmd160 = rmd160
	)
	f = open("../Portfile")
	out = open("Portfile", 'w')
	sub = Template(f.read()).safe_substitute(d)
	f.close()
	out.write(sub)
	out.close()
	
	os.chdir("..")
	
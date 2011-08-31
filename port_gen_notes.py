generating portfiles
base is arktools

list: 
	mavlink 
	arkcomm: mavlink
	arkmath
	arkosg: boost, qt, osg
	arkscicos: arkcomm, arkmath, arkosg
	
ports = {
	mavlink: {
		git-path: "pixhawk/mavlink"
		version: ""
		deps: [
		]
		descript: "Micro Air Vehicle communication library"
		long_descr: "MAVLink Micro Air Vehicle Message Marshalling Library \
		This is a library for lightweight communication between \
		Micro Air Vehicles (swarm) and/or ground control stations. \
		It serializes C-structs for serial channels and can be used with \
		any type of radio modem. \
		\
		Mailing list: http://groups.google.com/group/mavlink \
		More information: http://qgroundcontrol.org/mavlink/ \
		(c) 2009-2011 Lorenz Meier <mail@qgroundcontrol.org>"
	}
	arkcomm: {
		git-path: ""
		version: ""
		deps: [
			"mavlink"
		]
		descript: "Autonomous Robotics Kit communications library"
		long_descr: "Autonomous Robotics Kit communications library \
		http://arktools.github.com"
	}
	arkmath: {
		git-path: ""
		version: ""
		deps: [
		]
		descript: "Autonomous Robotics Kit math library"
		long_descr: "Autonomous Robotics Kit math library \
		http://arktools.github.com"
	}
	arkosg: {
		git-path: ""
		version: ""
		deps: [
			"boost",
			"qt-4-mac",
			"OpenSceneGraph"
		]
		descript: "Autonomous Robotics Kit, OpenSceneGraph library"
		long_descr: "Autonomous Robotics Kit, OpenSceneGraph library \
		http://arktools.github.com"
	}
	arcscicos: {
		git-path: ""
		version: ""
		deps: [
			"arkcomm",
			"arkmath",
			"arkosg"
		]
		descript: "Autonomous Robotics Kit, Scicoslab Toolbox"
		long_descr: "Autonomous Robotics Kit, Scicoslab Toolbox \
		http://arktools.github.com"
	}
}

from string import Template

foreach in list
	if directory doesnt exist:
		`git clone git@github.com:arktools/$name.git`
	`cd $name`
	`git pull`
	$id = `git rev-parse HEAD`
	$eight = substr($id, 0, 8)
	# eventually parse tag out of `git describe`
	download tar.gz
	get checksums of tar.gz
	
	make dict of templates to replace with safe_substitute: 
		$version
			for now, keep same for all? eventually parse from git tag
		$descript
			stored in hash
		$long_descr (wrap)
			stored in hash
		$depends (wrap)
			stored in hash
		$master_site
			http://github.com/arktools/$name/tarball/$id
		$filename
			arktools-$name-$eight
		$md5
		$sha1
		$rmd160
	
	open template (Portfile)
	open output ($name/Portfile)
	read template to Template()
	safe_substitute
	write to outfile
	close files
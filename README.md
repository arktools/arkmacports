Macports Portfile generator for arktools
=============
Author: Lenna X. Peterson (github.com/lennax)

### To generate Portfiles for: ###
 * arkcomm
 * arkmath
 * arkosg
 * arkscicos

```console
./gen_arktools.py
```

### User-definable variables ###
  (all caps in gen_arktools.py)
#### Development-related variables ####
 * LOCAL_PORT_TREE: path to local port tree (e.g. "~/ports")
 * PORTFILE_PATH: path to Portfile Template relative to gen_arktools.py

#### Port-related variables ####
 * in dict 'ports': 
   * DEPS: array of port dependencies
   * DESCRIPT: description
   * LONG_DESCR: long description (wrap with "\ \n    ")
 * GIT_PATH: organization/owner on github (e.g. "arktools")
 * HOMEPAGE: project website
 * VERSION: project version
 * CATEGORY: port category (e.g. "science")
 * PLATFORM: tested platforms (e.g. "darwin")
 * LICENSE: software license (e.g. "GPL-3") 
 * MAINTAINERS: port maintainers (obfuscated as example.com:you)
 * BUILD: ports required for building (e.g. "cmake")

#!/usr/bin/python

from string import Template

d = dict(name='lenna', age='23', food='coffee\n\tis delicious')
f = open("test.template")
# print d['name']

# dump = f.read()
# f.close() 
# sub = Template(dump).safe_substitute(d)
# out = open(d['name'], 'w')
# out.write(sub)
# out.close()

out = open(d['name'], 'w')
out.write(Template(f.read()).safe_substitute(d))
out.close()
f.close()
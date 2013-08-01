from unittest import TestCase, main

import os
import tempfile

from dynamic_pyyaml import YamlDict, YamlList, load

class TestDictionary(TestCase):
    def test_simple(self):
        res = YamlDict()
        res['a'] = 1
        res['b'] = 2
        
        self.assertEquals(res['a'], 1)
        self.assertEquals(res['b'], 2)
        self.assertEquals(res.a, 1)
        self.assertEquals(res.b, 2)
        self.assertEquals(res.items(), [('a', 1), ('b', 2)])
    
    def test_convertDict(self):
        res = YamlDict()
        res['a'] = 1
        res['b'] = YamlDict()
        res['b']['c'] = 3
        res['b']['d'] = 4
        
        self.assertEquals(res['a'], 1)
        self.assertEquals(res['b']['c'], 3)
        self.assertEquals(res['b']['d'], 4)
        self.assertEquals(res.a, 1)
        self.assertEquals(res.b.c, 3)
        self.assertEquals(res.b.d, 4)
    
    def test_resolveSimple(self):
        res = YamlDict()
        res['project_name'] = 'hello-world'
        res['home_dir'] = '/home/user'
        res['project_dir'] = '{home_dir}/projects/{project_name}'
        res.setAsRoot()
        
        self.assertEquals(res.project_name, 'hello-world')
        self.assertEquals(res.home_dir, '/home/user')
        self.assertEquals(res.project_dir, '/home/user/projects/hello-world')
    
    def test_resolveNested(self):
        res = YamlDict()
        res['project_name'] = 'hello-world'
        res['dirs'] = YamlDict()
        res['dirs']['home_dir'] = '/home/user'
        res['dirs']['project_dir'] = '{dirs.home_dir}/projects/{project_name}'
        res.setAsRoot()
        
        self.assertEquals(res.project_name, 'hello-world')
        self.assertEquals(res.dirs.home_dir, '/home/user')
        self.assertEquals(res.dirs.project_dir,
            '/home/user/projects/hello-world')
    
    def test_resolveLookup(self):
        res = YamlDict()
        res['project_name'] = 'hello-world'
        res['dirs'] = YamlDict()
        res['dirs']['home_dir'] = '/home/user'
        res['dirs']['project_dir'] = '{dirs.home_dir}/projects/{project_name}'
        res.setAsRoot()
        
        res.dirs.home_dir = '/winhome/user'
        
        self.assertEquals(res.project_name, 'hello-world')
        self.assertEquals(res.dirs.home_dir, '/winhome/user')
        self.assertEquals(res.dirs.project_dir,
            '/winhome/user/projects/hello-world')
    
    def test_orderedDictionary(self):
        fhndl, fname = tempfile.mkstemp()
        os.write(fhndl, 'a: 1\nb: 2\nc: 3\nd: 4\n')
        os.close(fhndl)
        
        res = load(open(fname))
        
        self.assertEquals(res.items(),
            [(u'a', 1), (u'b', 2), (u'c', 3), (u'd', 4)])
    
    def test_convertList(self):
        fhndl, fname = tempfile.mkstemp()
        os.write(fhndl, 'a: [1, 2, 3]\n')
        os.close(fhndl)
        
        res = load(open(fname))
        
        self.assertTrue(isinstance(res.a, YamlList))

class TestList(TestCase):
    def test_resolve(self):
        res = YamlList([1, '{%s[0]}'%YamlList.ROOT_NAME])
        
        self.assertEquals(res[0], 1)
        self.assertEquals(res[1], '1')
    
if __name__ == '__main__':
    import sys
    sys.exit(main())

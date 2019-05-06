from unittest import TestCase, main

import os
import tempfile

from dynamic_yaml import YamlDict, YamlList, load


class TestDictionary(TestCase):
    def test_simple(self):
        res = YamlDict()
        res['a'] = 1
        res['b'] = 2
        
        self.assertEqual(res['a'], 1)
        self.assertEqual(res['b'], 2)
        self.assertEqual(res.a, 1)
        self.assertEqual(res.b, 2)
        self.assertEqual(list(res.items()), [('a', 1), ('b', 2)])
    
    def test_convertDict(self):
        res = YamlDict()
        res['a'] = 1
        res['b'] = YamlDict()
        res['b']['c'] = 3
        res['b']['d'] = 4
        
        self.assertEqual(res['a'], 1)
        self.assertEqual(res['b']['c'], 3)
        self.assertEqual(res['b']['d'], 4)
        self.assertEqual(res.a, 1)
        self.assertEqual(res.b.c, 3)
        self.assertEqual(res.b.d, 4)
    
    def test_resolveSimple(self):
        res = YamlDict()
        res['project_name'] = 'hello-world'
        res['home_dir'] = '/home/user'
        res['project_dir'] = '{home_dir}/projects/{project_name}'
        res.set_as_root()
        
        self.assertEqual(res.project_name, 'hello-world')
        self.assertEqual(res.home_dir, '/home/user')
        self.assertEqual(res.project_dir, '/home/user/projects/hello-world')
    
    def test_resolveNested(self):
        res = YamlDict()
        res['project_name'] = 'hello-world'
        res['dirs'] = YamlDict()
        res['dirs']['home_dir'] = '/home/user'
        res['dirs']['project_dir'] = '{dirs.home_dir}/projects/{project_name}'
        res.set_as_root()
        
        self.assertEqual(res.project_name, 'hello-world')
        self.assertEqual(res.dirs.home_dir, '/home/user')
        self.assertEqual(res.dirs.project_dir, '/home/user/projects/hello-world')
    
    def test_resolveLookup(self):
        res = YamlDict()
        res['project_name'] = 'hello-world'
        res['dirs'] = YamlDict()
        res['dirs']['home_dir'] = '/home/user'
        res['dirs']['project_dir'] = '{dirs.home_dir}/projects/{project_name}'
        res.set_as_root()
        
        res.dirs.home_dir = '/winhome/user'
        
        self.assertEqual(res.project_name, 'hello-world')
        self.assertEqual(res.dirs.home_dir, '/winhome/user')
        self.assertEqual(res.dirs.project_dir, '/winhome/user/projects/hello-world')
    
    def test_orderedDictionary(self):
        fhndl, fname = tempfile.mkstemp()
        os.write(fhndl, 'a: 1\nb: 2\nc: 3\nd: 4\n'.encode('utf-8'))
        os.close(fhndl)

        with open(fname) as fileobj:
            res = load(fileobj)
            self.assertEqual(list(res.items()), [(u'a', 1), (u'b', 2), (u'c', 3), (u'd', 4)])
    
    def test_convertList(self):
        fhndl, fname = tempfile.mkstemp()
        os.write(fhndl, 'a: [1, 2, 3]\n'.encode('utf-8'))
        os.close(fhndl)

        with open(fname) as fileobj:
            res = load(fileobj)
            self.assertTrue(isinstance(res.a, YamlList))


class TestList(TestCase):
    def test_resolve(self):
        res = YamlList([1, '{{{}[0]}}'.format(YamlList.ROOT_NAME)])
        
        self.assertEqual(res[0], 1)
        self.assertEqual(res[1], '1')


if __name__ == '__main__':
    import sys
    sys.exit(main())

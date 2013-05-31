from unittest import TestCase, main

from dynamic_pyyaml import YamlDictionary, YamlList, load

class TestDictionary(TestCase):
    def test_simple(self):
        base = {'a': 1, 'b': 2}
        res = YamlDictionary(base)
        
        self.assertEquals(res['a'], base['a'])
        self.assertEquals(res['b'], base['b'])
        self.assertEquals(res.a, base['a'])
        self.assertEquals(res.b, base['b'])
        self.assertEquals(res.items(), [('a', 1), ('b', 2)])
    
    def test_convertDict(self):
        base = {'a': 1, 'b': {'c': 3, 'd': 4}}
        res = YamlDictionary(base)
        
        self.assertEquals(res['a'], base['a'])
        self.assertEquals(res['b']['c'], base['b']['c'])
        self.assertEquals(res['b']['d'], base['b']['d'])
        self.assertEquals(res.a, base['a'])
        self.assertEquals(res.b.c, base['b']['c'])
        self.assertEquals(res.b.d, base['b']['d'])
    
    def test_convertList(self):
        base = {'a': [1, 2, 3]}
        res = YamlDictionary(base)
    
        self.assertEquals(res.a[0], 1)
        self.assertEquals(res.a[1], 2)
        self.assertEquals(res.a[2], 3)
    
    def test_resolveSimple(self):
        base = {
            'project_name': 'hello-world',
            'home_dir': '/home/user',
            'project_dir': '{home_dir}/projects/{project_name}'
        }
        res = YamlDictionary(base)
        res.resolve()
        
        self.assertEquals(res.project_name, 'hello-world')
        self.assertEquals(res.home_dir, '/home/user')
        self.assertEquals(res.project_dir, '/home/user/projects/hello-world')
    
    def test_resolveNested(self):
        base = {
            'project_name': 'hello-world',
            'dirs': {
                'home_dir': '/home/user',
                'project_dir': '{dirs.home_dir}/projects/{project_name}'
            }
        }
        res = YamlDictionary(base)
        res.resolve()
        
        self.assertEquals(res.project_name, 'hello-world')
        self.assertEquals(res.dirs.home_dir, '/home/user')
        self.assertEquals(res.dirs.project_dir,
            '/home/user/projects/hello-world')
    
    def test_resolveLookup(self):
        base = {
            'project_name': 'hello-world',
            'dirs': {
                'home_dir': '/home/user',
                'project_dir': '{dirs.home_dir}/projects/{project_name}'
            }
        }
        res = YamlDictionary(base)
        res.update({'dirs': {'home_dir': '/winhome/user'}})
        res.resolve()
        
        self.assertEquals(res.project_name, 'hello-world')
        self.assertEquals(res.dirs.home_dir, '/winhome/user')
        self.assertEquals(res.dirs.project_dir,
            '/winhome/user/projects/hello-world')
    
    def test_orderedDictionary(self):
        import os
        import tempfile
        
        fhndl, fname = tempfile.mkstemp()
        os.write(fhndl, '!yaml_config\na: 1\nb: 2\nc: 3\nd: 4\n')
        os.close(fhndl)
        
        res = load(open(fname))
        
        self.assertEquals(res.items(), [('a', 1), ('b', 2), ('c', 3), ('d', 4)])

class TestList(TestCase):
    def test_simple(self):
        base = [1, 2, 3, 4]
        res = YamlList(base)
        
        self.assertEquals(res[0], 1)
        self.assertEquals(res[1], 2)
        self.assertEquals(res[2], 3)
        self.assertEquals(res[3], 4)
    
    def test_convertDict(self):
        base = [1, 2, {'a': 1, 'b': 2}]
        res = YamlList(base)
        
        self.assertEquals(res[0], 1)
        self.assertEquals(res[1], 2)
        self.assertEquals(res[2].a, 1)
        self.assertEquals(res[2].b, 2)
    
    def test_convertList(self):
        base = [1, [1, 2, 3]]
        res = YamlList(base)
        
        self.assertEquals(res[0], 1)
        self.assertTrue(isinstance(res[1], YamlList))

if __name__ == '__main__':
    import sys
    sys.exit(main())

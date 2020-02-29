from unittest import TestCase, main

from dynamic_yaml import load


class TestLoad(TestCase):
    def test_dict(self):
        config = '''
        a: 1
        b: 2
        c: 'a'
        '''
        res = load(config)
        self.assertDictEqual({'a': 1, 'b': 2, 'c': 'a'}, res)
    
    def test_nested_dict(self):
        config = '''
        a: 1
        b: 
          c: 3
          d: 4
          e: 'a'
        '''
        res = load(config)
        self.assertDictEqual({'a': 1, 'b': {'c': 3, 'd': 4, 'e': 'a'}}, res)
    
    def test_resolve_simple(self):
        config = '''
        project_name: hello-world
        home_dir: /home/user
        project_dir: '{home_dir}/projects/{project_name}'
        '''
        res = load(config)
        
        self.assertEqual('hello-world', res.project_name)
        self.assertEqual('/home/user', res.home_dir)
        self.assertEqual('/home/user/projects/hello-world', res.project_dir)
    
    def test_resolve_nested(self):
        config = '''
        project_name: hello-world
        dirs: 
          home_dir: /home/user
          project_dir: '{dirs.home_dir}/projects/{project_name}'
        '''
        res = load(config)
        
        self.assertEqual('hello-world', res.project_name)
        self.assertEqual('/home/user', res.dirs.home_dir)
        self.assertEqual('/home/user/projects/hello-world', res.dirs.project_dir)
    
    def test_resolve_simple_update(self):
        config = '''
        project_name: hello-world
        dirs: 
          home_dir: /home/user
          project_dir: '{dirs.home_dir}/projects/{project_name}'
        '''
        res = load(config)
        self.assertEqual('hello-world', res.project_name)
        self.assertEqual('/home/user', res.dirs.home_dir)
        self.assertEqual('/home/user/projects/hello-world', res.dirs.project_dir)

        res.dirs.home_dir = '/winhome/user'
        self.assertEqual('/winhome/user/projects/hello-world', res.dirs.project_dir)


if __name__ == '__main__':
    import sys
    sys.exit(main())

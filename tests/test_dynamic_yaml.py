from argparse import ArgumentParser
from unittest import TestCase, main

from dynamic_yaml import load


class TestDynamicYaml(TestCase):
    def test_list(self):
        config = '''
        - a
        - b
        - c
        '''
        res = load(config)
        self.assertEqual('a', res[0])
        self.assertEqual('b', res[1])
        self.assertEqual('c', res[2])

    def test_list_resolution(self):
        config = '''
        - a
        - b
        - '{root[0]}'
        '''
        res = load(config)
        self.assertEqual('a', res[0])
        self.assertEqual('b', res[1])
        self.assertEqual('a', res[2])

    def test_dict(self):
        config = '''
        a: 1
        b: 2
        c: a
        '''
        res = load(config)
        self.assertEqual(1, res.a)
        self.assertEqual(2, res.b)
        self.assertEqual('a', res.c)

        del res['a']
        self.assertNotIn('a', res)
        self.assertFalse(hasattr(res, 'a'))
        self.assertEqual(2, res.b)
        self.assertEqual('a', res.c)

        del res.b
        self.assertNotIn('b', res)
        self.assertFalse(hasattr(res, 'b'))
        self.assertEqual('a', res.c)

        delattr(res, 'c')
        self.assertNotIn('c', res)
        self.assertFalse(hasattr(res, 'c'))
    
    def test_nested_dict(self):
        config = '''
        a: 1
        b: 
          c: 3
          d: 4
          e: 'a'
        '''
        res = load(config)
        self.assertEqual(1, res.a)
        self.assertEqual(3, res.b.c)
        self.assertEqual(4, res.b.d)
        self.assertEqual('a', res.b.e)

    def test_deeply_nested_dict(self):
        config = '''
        a: 1
        b: 
          c: 2
          d: 3
          e:
            f: 4
            g:
              h: 5
        '''
        res = load(config)
        self.assertEqual(1, res.a)
        self.assertEqual(2, res.b.c)
        self.assertEqual(3, res.b.d)
        self.assertEqual(4, res.b.e.f)
        self.assertEqual(5, res.b.e.g.h)

    def test_resolve_simple(self):
        config = '''
        project_name: hello-world
        home_dir: /home/user
        project_dir: "{home_dir}/projects/{project_name}"
        '''
        res = load(config)

        self.assertEqual('hello-world', res.project_name)
        self.assertEqual('/home/user', res.home_dir)
        self.assertEqual('/home/user/projects/hello-world', res.project_dir)

    def test_resolve_missing(self):
        config = '''
        project_name: hello-world
        home_dir: /home/user
        project_dir: "{missing_dir}/projects/{project_name}"
        '''
        res = load(config)

        self.assertRaises(KeyError, lambda: res.project_dir)
    
    def test_resolve_nested(self):
        config = '''
        project_name: hello-world
        dirs: 
          home_dir: /home/user
          project_dir: "{dirs.home_dir}/projects/{project_name}"
        '''
        res = load(config)
        
        self.assertEqual('hello-world', res.project_name)
        self.assertEqual('/home/user', res.dirs.home_dir)
        self.assertEqual('/home/user/projects/hello-world', res.dirs.project_dir)

    def test_resolve_deeply_nested(self):
        config = '''
        project_name: hello-world
        dirs: 
          home_dir: /home/user
          project_dir: "{dirs.home_dir}/projects/{project_name}"
          tool1_output_dir: "{dirs.project_dir}/tool1-{parameters.tool1.phase1.subparameter1}-{parameters.tool1.phase1.subparameter2}"
        parameters:
          tool1:
            phase1:
              subparameter1: 0.5
              subparameter2: 1.6666
        '''
        res = load(config)

        self.assertEqual('/home/user/projects/hello-world/tool1-0.5-1.6666', res.dirs.tool1_output_dir)
    
    def test_resolve_simple_update(self):
        config = '''
        project_name: hello-world
        dirs: 
          home_dir: /home/user
          project_dir: "{dirs.home_dir}/projects/{project_name}"
        '''
        res = load(config)
        self.assertEqual('hello-world', res.project_name)
        self.assertEqual('/home/user', res.dirs.home_dir)
        self.assertEqual('/home/user/projects/hello-world', res.dirs.project_dir)

        res.dirs.home_dir = '/winhome/user'
        self.assertEqual('/winhome/user/projects/hello-world', res.dirs.project_dir)

    def test_resolve_nested_update(self):
        config = '''
        project_name: hello-world
        dirs: 
          home_dir: /home/user
          project_dir: "{dirs.home_dir}/projects/{project_name}"
        '''
        res = load(config)

        self.assertEqual('hello-world', res.project_name)
        self.assertEqual('/home/user', res.dirs.home_dir)
        self.assertEqual('/home/user/projects/hello-world', res.dirs.project_dir)

        res.dirs.database_dir = '{dirs.project_dir}/databases'
        res.databases = {'customers': '{dirs.database_dir}/customers.sqlite',
                         'items': '{dirs.database_dir}/items.sqlite'}
        self.assertEqual('/home/user/projects/hello-world/databases/customers.sqlite', res.databases.customers)
        self.assertEqual('/home/user/projects/hello-world/databases/items.sqlite', res.databases['items'])

    def test_argparse(self):
        config = '''
        output_dir: 'output-{parameters.parameter1}-{parameters.parameter2}'
        parameters:
          parameter1: a
          parameter2: b
        '''
        res = load(config)
        self.assertEqual('output-a-b', res.output_dir)

        parser = ArgumentParser()
        parser.add_argument('--parameter1')
        parser.add_argument('--parameter2')
        parser.parse_args(('--parameter1', 'c', '--parameter2', 'd'), namespace=res.parameters)
        self.assertEqual('output-c-d', res.output_dir)

    def test_recursive(self):
        config = '''
        prefix: /opt/ml
        input_path: '{prefix}/input'
        training_data_path: '{input_path}/data/training'
        '''

        res = load(config, recursive=True)
        self.assertEqual('/opt/ml/input', res.input_path)
        self.assertEqual('/opt/ml/input/data/training', res.training_data_path)

    def test_keyword_args(self):
        config = '''
        prefix: /opt/ml
        input_path: '{prefix}/input'
        training_data_path: '{input_path}/data/training'
        '''

        def inner_test(input_path, training_data_path, **kwargs):
            self.assertEqual('/opt/ml/input', input_path)
            self.assertEqual('/opt/ml/input/data/training', training_data_path)

        res = load(config, recursive=True)
        inner_test(**res)

    def test_list_iteration(self):
        config = '''
        targets:
          v1: value1
          v2: value2
        query:
          - '{targets.v1}'
          - '{targets.v2}'
        '''

        res = load(config)
        self.assertEqual(['value1', 'value2'], list(res.query))

    def test_dict_iteration(self):
        config = '''
        targets:
          v1: value1
          v2: value2
        query:
          v1: '{targets.v1}'
          v2: '{targets.v2}'
        '''

        res = load(config)
        self.assertEqual(['v1', 'v2'], list(res.query))
        self.assertEqual(['value1', 'value2'], list(res.query.values()))
        self.assertEqual([('v1', 'value1'), ('v2', 'value2')], list(res.query.items()))
    
    def test_multiline(self):
        config = '''
        a:
         a1: x
         a2: y
        b:
         b1: |
          line1
          line2 {a.a1}
         b2: line1 line2 {a.a2}
        '''
        res = load(config)
        self.assertEqual('line1 line2 y', res.b.b2)
        self.assertEqual('line1\nline2 x\n', res.b.b1)

    def test_merge_keys(self):
        config = '''
        a: &a
          b: value1
          f: '{d.e}'
        c:
          <<: *a
        d: 
          e: value2
        '''

        res = load(config)
        self.assertEqual('value1', res.c.b)
        self.assertEqual('value2', res.a.f)
        self.assertEqual('value2', res.c.f)


if __name__ == '__main__':
    import sys
    sys.exit(main())

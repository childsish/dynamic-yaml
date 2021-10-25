import yaml

from unittest import TestCase, main

from dynamic_yaml import load, dump


class TestDynamicYaml(TestCase):
    def test_json_dump(self):
        config = '''
        project_name: hello-world
        dirs: 
          home_dir: /home/user
          project_dir: "{dirs.home_dir}/projects/{project_name}"
          tool1_output_dir: "{dirs.project_dir}/tool1-{parameters.tool1.phase1.subparameters[0]}-{parameters.tool1.phase1.subparameters[1]}"
        parameters:
          tool1:
            phase1:
              subparameters:
               - 0.5
               - 0.6
            phase2:
              subparameters:
               - "{parameters.tool1.phase1.subparameters[0]}"
        '''
        res = load(config)
        self.assertEqual(
            yaml.safe_load('''
dirs:
  home_dir: /home/user
  project_dir: /home/user/projects/hello-world
  tool1_output_dir: /home/user/projects/hello-world/tool1-0.5-0.6
parameters: {tool1: {phase1: {subparameters: [0.5, 0.6]}, phase2: {subparameters: ['0.5']}}}
project_name: hello-world'''),
            yaml.safe_load(dump(res)))


if __name__ == '__main__':
    import sys

    sys.exit(main())

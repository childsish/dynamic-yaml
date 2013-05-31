Dynamic PyYAML
==============

Dynamic PyYAML is a couple of classes and functions that add extra functionality to YAML that turns it into a great configuration language for Python. YAML already provides:

* A very readable and clean syntax
* Infinitely nestable key:value pairs
* Sequence types
* A regulated portable syntax that conforms to strict standards

In addition, the PyYAML parser provides:

* Automatic type identification

Finally, the classes introduced by Dynamic PyYAML enable:

* Dynamic string resolution
* String resolution with supplied variables

Dynamic PyYAML requires PyYAML (https://bitbucket.org/xi/pyyaml).

Usage
-----
The key feature that was introduced is the ability for a string scalar to reference other parts of the configuration tree. This is done using the Python string formatting syntax. The characters '{' and '}' enclose a reference to another entry in the configuration structure. The reference takes the form key1.key2 where key1 maps to another mapping object and can be found in the root mapping, and key2 can be found in key1's mapping object.

An example yaml configuration:
```yaml
!yaml_config
project_name: hello-world
dirs:
    home: /home/user
    venv: "{dirs.home}/venvs/{project_name}"
    bin: "{dirs.venv}/bin"
    data: "{dirs.venv}/data"
    errors: "{dirs.data}/errors"
    sessions: "{dirs.data}/sessions"
    databases: "{dirs.data}/databases"
exes:
    main: "{dirs.bin}/main"
    test: "{dirs.bin}/test"
bases_per_chromosome:
    - 30432563
    - 19705359
    - 23470805
    - 18585042
    - 26992728
    - 154478
    - 366924
```
Example python code reading the configuration:
```python
>>> from dynamic_pyyaml import load
>>> cfg = load(open('cfg.yaml'))
>>> print cfg.exes.main
/home/user/venvs/hello-world/bin/main
>>> cfg = load(open('cfg.yaml'), {
...     'project_name': 'goodbye',
...     'dirs': {
...         'home': '/home/another_user'
...     }
... })
>>> print cfg.exes.main
/home/another_user/venvs/goodbye/bin/main
```

Restrictions
------------

Due to the short amount of time I was willing to spend on working upon this, there are a few restrictions required for a valid YAML configuration file.

* **The first line must be the string "!yaml_config".** This is a YAML tag that tells the PyYAML loader to create a configuration object from the file.
* **Wild card strings must be surrounded by quotes.** Braces ('{' and '}') in a YAML file usually enclose a mapping object. However, braces are also used by the Pyhton string formatting syntax to enclode a reference. As there is no way to change either of these easily, strings that contain wildcards must be explicitly declared using single or double quotes to enclose them.
* **The root node must be key:value pairs.** I was simply too lazy to allow sequence types as the root node.
* **Dependencies must be declared in the order that they are to be resolved.** This was also due to time constraints. In future, a fancy dependency resolution graph could be constructed, but at the moment, I think it works well as it is.

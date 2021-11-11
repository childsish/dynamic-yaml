![](https://github.com/childsish/dynamic-yaml/workflows/Project%20Tests/badge.svg)

dynamic-yaml
============

Dynamic YAML is a couple of classes and functions that add extra functionality to YAML that turns it into a great configuration language for Python. If you prefer JSON, then see [dynamic-json][dynamic-json].

YAML already provides:

* A very readable and clean syntax
* Infinitely nestable key:value pairs
* Sequence types
* A regulated portable syntax that conforms to strict standards

In addition, the PyYAML parser provides:

* Automatic type identification (a result of implementing the YAML standard)

Finally, the classes introduced by Dynamic YAML enable:

* Dynamic string resolution

Dynamic PyYAML requires PyYAML (https://bitbucket.org/xi/pyyaml).

Usage
-----

The key feature that was introduced is the ability for a string scalar to reference other parts of the configuration tree.
This is done using the Python string formatting syntax.
The characters '{' and '}' enclose a reference to another entry in the configuration structure.
The reference takes the form key1.key2 where key1 maps to another mapping object and can be found in the root mapping, and key2 can be found in key1's mapping object.
Multiple levels of nesting can be used (eg. key1.key2.key3 etc...).
If you need brace literals, they can be escaped by doubling them up, as described by the Python format string [documentation](https://docs.python.org/3/library/string.html#formatstrings). 

An example yaml configuration:
```yaml
project_name: hello-world
dirs:
    home: /home/user
    venv: "{dirs.home}/venvs/{project_name}"
    bin: "{dirs.venv}/bin"
    data: "{dirs.venv}/data"
    errors: "{dirs.data}/errors"
    sessions: "{dirs.data}/sessions"
    databases: "{dirs.data}/databases"
    output: "{dirs.data}/output-{parameters.parameter1}-{parameters.parameter2}"
exes:
    main: "{dirs.bin}/main"
    test: tests
parameters:
    parameter1: a
    parameter2: b
```

Reading in a yaml file:

```python
import dynamic_yaml

with open('/path/to/file.yaml') as fileobj:
    cfg = dynamic_yaml.load(fileobj)
    assert cfg.dirs.venv == '/home/user/venvs/hello-world'
    assert cfg.dirs.output == '/home/user/venvs/hello-world/data/output-a-b'
```

As the variables are dynamically resolved, it is also possible to combine this with `argparse`:

```python
import dynamic_yaml

from argparse import ArgumentParser

with open('/path/to/file.yaml') as fileobj:
    cfg = dynamic_yaml.load(fileobj)
    parser = ArgumentParser()
    parser.add_argument('--parameter1')
    parser.add_argument('--parameter2')
    parser.parse_args('--parameter1 c --parameter2 d'.split(), namespace=cfg.parameters)
    assert cfg.dirs.output == '/home/user/venvs/hello-world/data/output-c-d'
```

Writing yaml will resolve all references:

```python
import dynamic_yaml
import yaml

with open('/path/to/file.yaml') as fileobj:
    cfg = dynamic_yaml.load(fileobj)
    assert yaml.safe_load(dynamic_yaml.dump(cfg)) == yaml.safe_load('''
project_name: hello-world
dirs:
    home: /home/user
    venv: /home/user/venvs/hello-world
    bin: /home/user/venvs/hello-world/bin
    data: /home/user/venvs/hello-world/data
    errors: /home/user/venvs/hello-world/data/errors
    sessions: /home/user/venvs/hello-world/data/sessions
    databases: /home/user/venvs/hello-world/data/databases
    output: /home/user/venvs/hello-world/data/output-a-b}
exes:
    main: /home/user/venvs/hello-world/bin/main
    test: tests
parameters:
  - 0.5
  - 0.1
''')
```

Installation
------------

To install, simply run:

```bash
pip install dynamic-yaml
```

Restrictions
------------

Due to the short amount of time I was willing to spend on working upon this, there are a few restrictions that I could not overcome.

* **Wild card strings must be surrounded by quotes.**
Braces ('{' and '}') in a YAML file usually enclose a mapping object.
However, braces are also used by the Python string formatting syntax to enclose a reference.
As there is no way to change either of these easily, strings that look like a yaml mapping must be explicitly declared using single or double quotes to enclose them.
For example:
  ```yaml
  quotes_needed: '{variable}'
  ```
* **Certain keys can only be used via `__getitem__` and not `__getattr__`.**
Because `dict` comes with it's own set of attributes that are always resolved first, the values for the following keys must be gotten using the item getter rather than the attribute getter (eg. config['items'] vs. config.items):
  * append
  * extend
  * insert
  * remove
  * pop
  * clear
  * index
  * count
  * sort
  * reverse
  * copy 

[dynamic-json]: https://github.com/childsish/dynamic-json

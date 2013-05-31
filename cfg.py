{
    'project_name': 'hello-world',
    'dirs': {
        'home': '/home/user',
        'venv': '{dirs.home}/venvs/{project_name}',
        'bin': '{dirs.venv}/bin',
        'data': '{dirs.venv}/data',
        'errors': '{dirs.data}/errors',
        'sessions': '{dirs.data}/sessions',
        'databases': '{dirs.data}/databases'
    },
    'exes': {
        'main': '{dirs.bin}/main',
        'test': '{dirs.bin}/test',
    },
    'bases_per_chromosome': [
        30432563,
        19705359,
        23470805,
        18585042,
        26992728,
        154478,
        366924
    ]
}

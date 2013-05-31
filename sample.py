from dynamic_pyyaml import load

cfg = load(open('cfg.yaml'))
print cfg.exes.main
cfg = load(open('cfg.yaml'), {
    'project_name': 'goodbye',
    'dirs': {
        'home': '/home/another_user'
    }
})
print cfg.exes.main

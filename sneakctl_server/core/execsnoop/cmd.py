execsnoop_options = {
    'time': {
        'variations': ('--time', '-t'),
        'has_arg': False
    },
    'timestamp': {
        'variations': ('--timestamp', '-T'),
        'has_arg': False
    },
    'username': {
        'variations': ('-u', '--uid'),
        'has_arg': True
    },
    'fails': {
        'variations': ('-x', '--fails'),
        'has_arg': False
    },
    'cgroupmap': {
        'variations': ('--cgroupmap',),
        'has_arg': True
    },
    'mntnsmap': {
        'variations': ('--mntnsmap',),
        'has_arg': True
    },
    'quote': {
        'variations': ('-q', '--quote'),
        'has_arg': False
    },
    'name': {
        'variations': ('-n', '--name'),
        'has_arg': True
    },
    'line': {
        'variations': ('-l', '--line'),
        'has_arg': True
    },
    'print_uid': {
        'variations': ('-U', '--print-uid'),
        'has_arg': False
    },
    'max_args': {
        'variations': ('--max-args',),
        'has_arg': True
    }
}
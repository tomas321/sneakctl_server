tcptracer_options = {
    'timestamp': {
        'variations': ('--timestamp', '-t'),
        'has_arg': False
    },
    'process_id': {
        'variations': ('-p', '--pid'),
        'has_arg': True
    },
    'netns': {
        'variations': ('-N', '--netns'),
        'has_arg': True
    },
    'cgroupmap': {
        'variations': ('--cgroupmap',),
        'has_arg': True
    },
    'mntnsmap': {
        'variations': ('--mntnsmap',),
        'has_arg': True
    },
    'verbose': {
        'variations': ('-v', '--verbose'),
        'has_arg': False
    },
}

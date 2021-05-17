fswatch_options = {
    'time_format': {
        'variations': ('-f', '--format-time'),
        'has_arg': True
    },
    'timestamp': {
        'variations': ('--timestamp', '-T'),
        'has_arg': False
    },
    'latency': {
        'variations': ('-l', '--latency'),
        'has_arg': True
    },
    'follow_links': {
        'variations': ('-L', '--follow-links'),
        'has_arg': False
    },
    'recursive': {
        'variations': ('-r', '--recursive'),
        'has_arg': False
    },
    'utc': {
        'variations': ('-u', '--utc-time'),
        'has_arg': False
    },
    'event_flags': {
        'variations': ('-x', '--event-flags'),
        'has_arg': False
    },
    'exclude_event': {
        'variations': ('--ex-event',),
        'has_arg': True
    },
    'event': {
        'variations': ('--event',),
        'has_arg': True
    },
    'verbose': {
        'variations': ('-v', '--verbose'),
        'has_arg': False
    }
}

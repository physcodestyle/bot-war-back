def extract_settings(args):
    settings = {
        'host': '',
        'port': '',
    }
    for s in dict.keys(settings):
        for a in args:
            if a.startswith(f'--{s}') or a.startswith(f'-{s[0]}'):
                settings[s] = a.split('=')[1]
    return settings
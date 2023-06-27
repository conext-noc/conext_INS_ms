def filler(dict_host, dict_filler):
    for key in dict_host:
        dict_host[key] = dict_filler[key]

    return dict_host

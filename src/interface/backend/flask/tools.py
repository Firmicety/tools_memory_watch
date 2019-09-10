def get_resource_usage():
    import json
    with open("useage.json") as f:
        data = json.load(f)
    return data

def get_configuration():
    units_translation = {"KB":1, "MB": 1024, "GB": 1048576}
    data = {}
    with open("configurations/user_resources.conf") as f:
        for lines in f:
            username, volumn, unit = lines.rstrip().split(' ')
            data[username] = int(volumn)*units_translation[unit]
    return data
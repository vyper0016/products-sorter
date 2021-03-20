import json


def sort_json(file_input, file_output):
    with open(file_input, 'r') as f:
        data = json.load(f)

    sor = sorted(data.items(), key=lambda x: x[1]['rate'])

    clean_sor = {}

    for i in sor:
        clean_sor[i[0]] = i[1]

    with open(file_output, 'w') as df:
        json.dump(clean_sor, df, indent=3)

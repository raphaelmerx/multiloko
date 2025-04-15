"""
Copyright (c) Meta Platforms, Inc. and affiliates.

This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
#!/usr/bin/env python3
from sys import argv
import json
import csv

with open(argv[1], 'r') as infilejson, open(argv[2], 'w') as outfilejson, open(argv[3], 'w') as outfilecsv:
    output = []
    data = json.load(infilejson)
    for lang in data:
        mylang = lang.replace('_dev', "")
        for example in data[lang]:
            output.append({'language': mylang, 'id': example['id'], 'prediction': example['prediction']})

    csvwriter = csv.DictWriter(outfilecsv, fieldnames=['language', 'id', 'prediction'])
    csvwriter.writeheader()
    for line in output:
        outfilejson.write(json.dumps(line, ensure_ascii=False) + '\n')
        csvwriter.writerow(line)

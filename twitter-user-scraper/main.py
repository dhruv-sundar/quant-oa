from user import verify, dictify
import sys
import json

TARGET = sys.argv[1]
verify(TARGET)

with open("output.json", "w") as outfile:
    json.dump(dictify(TARGET), outfile, indent=4)

print("Written to output.json")
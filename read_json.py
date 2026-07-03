import json

with open("data.json", "r") as file:
    data = json.load(file)

print("Project:", data["projectName"])
print("Owner:", data["owner"])
print("Version:", data["version"])
print("Active:", data["active"])
print("Languages:")

for language in data["languages"]:
    print("-", language)

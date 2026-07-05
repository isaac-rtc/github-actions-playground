import json

with open("data.json", "r") as file:
    data = json.load(file)

description = data["repository"]["description"]
homepage = data["repository"]["homepage"]

print("Description:", description)
print("Homepage:", homepage)

payload = {
    "description": description,
    "homepage": homepage
}

print("Payload GitHub expects:")
print(json.dumps(payload, indent=2))

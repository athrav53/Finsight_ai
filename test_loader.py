from modules.config_loader import load_config

config = load_config("test.json")

print(config)
print(config["name"])
print(config["version"])
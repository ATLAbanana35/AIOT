import logging
import json

f = open("config.json")
config = json.load(f)
f.close()
f = open("av_config.json")
advanced_config = json.load(f)
f.close()

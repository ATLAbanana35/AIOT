from config.aiotconfig import advanced_config, config
from api.homeassistant.main import client
import logging
import os
from homeassistant_api import *


def analyse_prompt(prompt: str, safeMode: bool = False):
    if prompt.lower().startswith("error"):
        error = prompt.split(":")[1:].join(":")
        logging.error("Problem during prompt generation: ", error)
        return "ERROR: " + error
    if not (safeMode):
        try:
            exec(prompt, globals())
            return globals().get("result", None)
        except Exception as e:
            return "ERROR: " + str(e)

    else:
        f = open("tmp/f.py", "w+", encoding="utf-8")
        f.write(prompt)
        f.close()
        error = os.system("python -m py_compile tmp/f.py")
        os.remove("tmp/f.py")
        if error == 0:
            return "Prompt: OK"
        else:
            return "ERROR: PROMPT CONTAINS SYNTAX ERROR"

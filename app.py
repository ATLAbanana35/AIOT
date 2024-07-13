from main.mainclass import AIOT
from utils.startmessage import ShowStartMessage
import logging
from config.aiotconfig import config
import os
from config.commands import commands
from api.homeassistant.main import client
from utils.colorOut import CustomFormatter

logLevel = config["log_level"]
logging.basicConfig(
    filename="logs/app.log",
    filemode="a+",
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.getLevelName(logLevel),
)
ch = logging.StreamHandler()
ch.setLevel(logging.getLevelName(logLevel))
ch.setFormatter(CustomFormatter())

logging.getLogger().addHandler(ch)

logging.info("Program started ")

logging.debug("Initializing Main Class...")

ShowStartMessage()

aiotClass = AIOT()

print("AIOT CLI: ")


def main():
    try:
        aiotCMD = input(os.getcwd() + " #:")
        splitCMD = aiotCMD.split(" ")
        if splitCMD[0] in commands:
            out = commands[f"{splitCMD[0]}"](splitCMD[1:])
            if out:
                out()
        else:
            logging.warning("Command not found (" + splitCMD[0] + ")")
        main()
    except Exception as e:
        logging.error(e)
        main()


main()

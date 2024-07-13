from api.homeassistant.main import client
import logging
from config.aiotconfig import config, advanced_config
import json
from server.httpserver import run
import threading
from utils.variables import server_thread, kill_switch
from ai.prompt_gen import GeneratePrompt
from ai.prompt_analise import analyse_prompt
from ai.ai_learn import LearnPrincState, LearnAttributeState


def cmd_command_testAPI(args):
    logging.info("Checking API status for " + client.api_url)
    if client.check_api_running():
        return lambda: logging.info("OK: API is Running!")
    else:
        return lambda: logging.error(
            "ERROR: API is NOT Running please rewrite your config with gen-config"
        )


def cmd_command_updateAVConfig(args):
    logging.info("Updating config: Asking parameters")
    confUp = {}
    for conf in advanced_config:
        confUp[conf] = input('Enter "' + conf + '" value: ')
    f = open("av_config.json", "w")
    f.write(json.dumps(confUp))
    f.close()
    return lambda: logging.warn("A reload is required for applying the config!")


def cmd_command_updateConfig(args):
    logging.info("Updating advanced_config: Asking parameters")
    confUp = {}
    for conf in config:
        confUp[conf] = input('Enter "' + conf + '" value: ')
    f = open("config.json", "w")
    f.write(json.dumps(confUp))
    f.close()
    return lambda: logging.warn("A reload is required for applying the config!")


def cmd_command_runPY(code):
    return lambda: logging.warn("Returned value: " + str(eval(" ".join(code))))


def cmd_command_startServer(args):
    run(port=int(config["port"]))
    return lambda: logging.warn("Server Started!")


def cmd_command_exit(args):
    global kill_switch
    kill_switch = True
    logging.warn("Server Stopped!")
    return lambda: exit()


def cmd_command_startServerInBackground(args):
    global server_thread
    thread = threading.Thread(target=run, args=(int(config["port"]),))
    thread.start()
    server_thread = thread
    return lambda: logging.warn(
        "Server Started (in background) /!\ will close with program <NOT DAEMON>)!"
    )


def cmd_command_ai_playground(args):
    logging.debug("Starting AI PLAYGROUND...")
    print(" █████╗ ██╗")
    print("██╔══██╗██║")
    print("███████║██║----PLAYGROUND")
    print("██╔══██║██║")
    print("██║  ██║██║")
    print("╚═╝  ╚═╝╚═╝")
    print("\n")
    print("\n")
    print("Enter Option:")
    print("[1]: Print prompts")
    print("[2]: Generate prompt")
    print("[3]: Check AI answer, running-free (Safe Mode)")
    print("[4]: Check AI answer, WITH running the commands")
    print("[5]: Learn a new state of an object")
    print(
        "[6]: Learn a new state of an attribute of an object (like: color of a light)"
    )
    print("[e]: exit")
    print("\n")
    answer = input("Enter your choice: ")
    if answer == "e":
        return lambda: logging.debug("Exiting AI playground")
    if answer == "1":
        logging.debug("AI_PLAYGROUND: USER ASKED FOR Printing prompts")
        print("Main Prompt: ", advanced_config["prompt_f"])
        print("Entity Prompt: ", advanced_config["entity_give"])
    if answer == "2":
        ask = input("What do you want to ask: ")
        knowing = input("Do your AI know the homeassistant python library? (y/n): ")
        if knowing == "y":
            print("Prompt Generated: ", GeneratePrompt(ask, True))
            logging.debug("A prompt was generated")
        else:
            print("Prompt Generated: ", GeneratePrompt(ask, False))
            logging.debug("A prompt was generated")
    if answer == "5":
        LearnPrincState()
    if answer == "6":
        LearnAttributeState()
    if answer == "3":
        logging.debug("Analyzing prompt (Safe-Mode)...")
        print("Enter/Paste your AI answer. Ctrl-D or Ctrl-Z ( windows ) to save it.")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)
        print(analyse_prompt("\n".join(contents), safeMode=True))
    if answer == "4":
        logging.debug("Analyzing prompt (Execution-Mode)...")
        print("Enter/Paste your AI answer. Ctrl-D or Ctrl-Z ( windows ) to save it.")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)
        print(analyse_prompt("\n".join(contents)))
    input("[ENTER] to continue...")
    cmd_command_ai_playground(args)


commands = {
    "/status": cmd_command_testAPI,
    "/run": cmd_command_runPY,
    "/exit": cmd_command_exit,
    "/start": cmd_command_startServer,
    "/ai": cmd_command_ai_playground,
    "/start_bg": cmd_command_startServerInBackground,
    "/gen-config": cmd_command_updateConfig,
    "/av-gen-config": cmd_command_updateAVConfig,
}

from api.homeassistant.main import client
from config.aiotconfig import advanced_config
import json
import logging


def LearnPrincState():
    print("IDS: ")
    ids = {}
    i = 0
    states = client.get_states()
    for id in states:
        i += 1
        ids[i] = [id.entity_id, id.state]
        print("[" + str(i) + "]: " + id.entity_id)
    id = input("Choose an object: ")
    if ids[int(id)]:
        input("Put the object in the desired state, then press [ENTER]")
        sts = client.get_entity(entity_id=ids[int(id)][0]).get_state().state
        if (
            input(
                "The learned state for the desired object is "
                + sts
                + " is that alright (y) "
            )
            == "y"
        ):
            if [ids[int(id)][0]][0] in advanced_config["learned"]:
                advanced_config["learned"][ids[int(id)][0]].append(sts)
            else:
                advanced_config["learned"][ids[int(id)][0]] = [sts]
            f = open("av_config.json", "w")
            f.write(json.dumps(advanced_config))
            f.close()
            logging.debug("New object learned!")


def LearnAttributeState():
    print("IDS: ")
    ids = {}
    i = 0
    states = client.get_states()
    for id in states:
        i += 1
        ids[i] = [id.entity_id, id.state]
        print("[" + str(i) + "]: " + id.entity_id)
    id = input("Choose an object: ")
    if ids[int(id)]:
        input("Put the object in the desired state, then press [ENTER]")
        attr = client.get_state(entity_id=ids[int(id)][0]).attributes
        i = 0
        attrs = {}
        for att in attr:
            i += 1
            attrs[i] = att
            print(f"[{i}] Attribute {att} is {attr[att]}")
        choice = int(input("Choose an attribute to learn: "))
        if attrs[choice]:
            if (
                input(
                    "The learned attribute ("
                    + attrs[choice]
                    + ") for the desired object is "
                    + str(attr[attrs[choice]])
                    + " is that alright (y) "
                )
                == "y"
            ):
                if advanced_config["learned_attrs"][ids[int(id)][0]]:
                    advanced_config["learned_attrs"][ids[int(id)][0]] = {}
                if (
                    advanced_config["learned_attrs"][ids[int(id)][0]][attrs[choice]]
                    in advanced_config["learned"]
                ):
                    advanced_config["learned_attrs"][ids[int(id)][0]][attrs[choice]] = (
                        "value, for ex: " + str(attr[attrs[choice]])
                    )
                else:
                    advanced_config["learned_attrs"][ids[int(id)][0]] = {
                        attrs[choice]: "value, for ex: " + str(attr[attrs[choice]])
                    }
                f = open("av_config.json", "w")
                f.write(json.dumps(advanced_config))
                f.close()
                logging.debug("New attribute learned!")

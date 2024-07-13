from config.aiotconfig import advanced_config, config
from api.homeassistant.main import client

system_prompt = advanced_config["prompt_f"]

entity_prompt = advanced_config["entity_give"]


def GeneratePrompt(user_demand, know_doc=True):
    entire_prompt = system_prompt
    if know_doc:
        entire_prompt = entire_prompt.replace("[KNOW]", "")
    else:
        entire_prompt = entire_prompt.replace(
            "[KNOW]",
            "This is an example of the homeassistant python lib: "
            + advanced_config["example"],
        )
    entities_prompt = ""
    for state in client.get_states():
        entities_prompt += entity_prompt.replace("[Type]", state.entity_id).replace(
            "[State]", state.state
        )
    custom_prompt = "The following ids and states can be used to place objects in the desired states A STATE OF A TYPE OF OBJECT CAN BE USED ON A SAME TYPE OBJECT (Ex: vacuum roborock s6 to s8): "
    for id_ in advanced_config["learned"]:
        custom_prompt += ", " + id_ + ":" + ";".join(advanced_config["learned"][id_])
    custom_prompt += "The following ids and states can be used to place attributes of objects in the desired states: "
    for id_ in advanced_config["learned_attrs"]:
        custom_prompt += ", " + id_ + ":"
        for i_ in advanced_config["learned_attrs"][id_]:
            custom_prompt += (
                i_ + ":" + str(advanced_config["learned_attrs"][id_][i_]) + ";"
            )
    entire_prompt = (
        entire_prompt.replace("[ENTITIES]", entities_prompt)
        .replace("[USER_ASK]", user_demand)
        .replace("[LANG]", config["language"])
        .replace("[CUSTOM]", advanced_config["custom"] + " " + custom_prompt)
    )
    return entire_prompt

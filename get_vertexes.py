from inspect import isclass
from pprint import pprint
import json
import math
import random
import string
from langflow.utils.util import get_base_classes


# vertex_classes = {
#     "PromptTemplate": ['template'],
#     "OpenAI": ['model_name', 'temperature', 'max_tokens', 'openai_api_key'],
#     "TextRequestsWrapper": ['memory', 'llm', 'prompt'],
# }

vertex_classes = [
    "PromptTemplate",
    "OpenAI",
    "TextRequestsWrapper",
    "JsonSpec",
    "JsonToolkit",
    "create_json_agent",
    "AgentExecutor",
]


def create_vertex(vertex):
    """This function is to create dictionary of all the inputs in an
    instance in required format"""
    vertex_key = type(vertex).__name__
    parameters_dict = {}

    # get the kwargs from the variable list
    for i in vertex:
        try:
            if i[0] == "lc_kwargs":
                kwargs = i[1].keys()
                break
        except:
            pass

    for i in vertex:
        temp = {
            "required": False,
            "placeholder": "",
            "show": False,
            "multiline": False,
            "value": 0,
            "password": False,
            "name": "temperature",
            "advanced": False,
            "type": "float",
            "list": False,
        }

        if i[0] == "lc_kwargs":
            # showing only lc_kwargs
            # kwargs = i[1].keys()
            continue

        temp["name"] = i[0]
        if isinstance(i[1], set):
            temp["value"] = list(i[1])
            temp["type"] = type(i[1]).__name__
            continue

        if isclass(i[1]):
            temp["value"] = type(i[1]).__name__
        else:
            temp["value"] = i[1]

        temp["type"] = type(i[1]).__name__
        # temp["value"] = i[1]

        if type(i[1]).__name__ in vertex_classes:
            temp["value"] = type(i[1]).__name__

        # # check it should have shown in flow or not
        try:
            if i[0] in kwargs:
                temp["show"] = True
                temp["required"] = True

        except:
            pass
        parameters_dict[i[0]] = temp

    parameters_dict["_type"] = vertex_key
    return vertex_key, parameters_dict


def update_all_info(vertex, vertex_key, parameter_dict, coordinates):
    """Function create nodes info for a vertex"""
    with open("Base_flows/vertex_all_info.json", "r") as file:
        vertex_all_info = json.load(file)

    # generate id suffix
    id_suffix = generate_random_string()
    vertex_id = vertex_key + "_" + id_suffix

    # get base classes
    base_classes = get_base_classes(vertex.__class__)

    vertex_all_info["type"] = "genericNode"
    vertex_all_info["id"] = vertex_id
    vertex_all_info["data"]["type"] = vertex_key
    vertex_all_info["data"]["node"]["template"] = parameter_dict
    vertex_all_info["data"]["node"]["base_classes"] = base_classes
    vertex_all_info["data"]["id"] = vertex_id

    vertex_all_info["position"]["x"] = coordinates[0]
    vertex_all_info["position"]["y"] = coordinates[1]

    # create specific info needed for edges creations
    vertex_edge_info = [vertex_key, vertex_id] + base_classes

    return vertex_all_info, vertex_edge_info


def update_baseflow_vertexes(base_flow, all_instances):
    """Update the vertex_all_info for all instances"""
    # get the coordinates for the components
    coordinates = allocate_components(len(all_instances))
    vertex_edge_info_dict = {}
    for index, vertex in enumerate(all_instances):
        vertex_key, parameter_dict = create_vertex(vertex)
        vertex_all_info_json, vertex_edge_info = update_all_info(
            vertex, vertex_key, parameter_dict, coordinates[index]
        )
        # create the dict file for edge info
        vertex_edge_info_dict[vertex_key] = vertex_edge_info
        # update base flow nodes
        base_flow["data"]["nodes"].append(vertex_all_info_json)

    return base_flow, vertex_edge_info_dict


def allocate_components(num_components):
    """Allocate the vertexes"""
    components = []
    n_nodes = 4
    shift = num_components // n_nodes
    init_x = 400
    init_y = 400
    for s in range(shift + 1):
        for i in range(n_nodes):
            angle = i * (2 * math.pi / n_nodes)
            x = (s - 1) * 30 + init_x * math.cos(math.pi - angle)
            y = init_y * math.sin(angle)
            components.append((x, y))

    return components[:num_components]


def generate_random_string(length=5):
    lowercase_chars = string.ascii_lowercase + string.digits
    random_string = "".join(random.choice(lowercase_chars) for _ in range(length))
    return random_string


def is_instance_from_langchain(class_obj, module_name):
    try:
        class_module_parts = class_obj.__module__.split(".")
        module_parts = module_name.split(".")

        # Compare the last parts of the module names
        if module_name in class_module_parts:
            return True
        else:
            return False
    except:
        return False

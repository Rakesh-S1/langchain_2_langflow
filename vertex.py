from langflow.interface.types import build_langchain_types_dict
import uuid
import string
import random, math
from langflow.utils import util
import inspect
# get templates of all the vertexes available
all_vertex_template = build_langchain_types_dict()


all_vertex_info  = {}
def generate_random_string(length=5):
    lowercase_chars = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choice(lowercase_chars)
                            for _ in range(length))
    return random_string


def get_base_class():
    id = str(uuid.uuid4())
    base_data = {
        "description": "Design Dialogues with LangFlow.",
        "name": "Modest Franklin",
        "data": {"nodes": [],
                 "edges": [],
                 "viewport": {"x": 1, "y": 0, "zoom": 0.5}
                 },
        "id": id
    }
    return base_data

vertex_info_dict = {}
def get_template(component_name: str, vertex_name: str,vertex=None,position=None,lc_kwargs=None) -> dict | None:
    try:
        for key in all_vertex_template[component_name]:
            if key.lower() == vertex_name.lower():
                vertex_id = f"{vertex_name}_{generate_random_string()}"
                Node = {
                    "width": 0,
                    "height": 0,
                    "id": vertex_id,
                    "type": "genericNode",
                    "position": {"x": position[0], "y": position[1]},
                    "data": {"type": key, "node": {}, "id": vertex_id, "value": None},
                    "positionAbsolute": {"x": position[0], "y": position[1]},
                }
                dict_data = all_vertex_template[component_name][key]
                for key, value in dict_data.items():
                    Node["data"]["node"][key] = value

                # update vertex_info_dict
                all_vertex_info[vertex_id] = {
                    'vertex_name': vertex_name,
                    'vertex_id': vertex_id,
                    'component_name': component_name,
                    'vertex': vertex,
                    'base_class': util.get_base_classes(vertex.__class__),
                    'children': []
                }

                # get input values from langchain code
                if lc_kwargs:
                    for key, value in lc_kwargs.items():
                        if is_instance_from_langchain(type(value), "langchain"):
                            continue

                        if key in Node["data"]["node"]["template"].keys():
                            Node["data"]["node"]["template"][key]["value"] = lc_kwargs[key]

                return Node
    except:
        pass



def allocate_components(num_components):
    """ Allocate the vertexes """
    components = []
    n_nodes = 4
    shift = num_components // n_nodes
    init_x = 400
    init_y = 400
    for s in range(shift+1):
        for i in range(n_nodes):
            angle = i * (2*math.pi / n_nodes)
            x = (s-1) * 30 + init_x * math.cos(math.pi-angle)
            y = init_y * math.sin(angle)
            components.append((x, y))

    return components[:num_components]


def is_instance_from_langchain(class_obj, module_name):
    try:
        class_module_parts = class_obj.__module__.split('.')
        module_parts = module_name.split('.')

        # Compare the last parts of the module names
        if module_name in class_module_parts:
            return True
        else:
            return False
    except:
        return False
import inspect
import importlib.util
import json
import langchain
import copy
from vertex import (get_template, get_base_class,
                    allocate_components,
                    is_instance_from_langchain,
                    all_vertex_info)

from utils import SetEncoder
from edges import get_children, create_edges
from pprint import  pprint

# input file path
python_file_path = "input.py"

# get classes and instances from the input file
module_name = "custom_module"
spec = importlib.util.spec_from_file_location(module_name, python_file_path)
custom_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(custom_module)

# get class objects
class_list = []
function_list = []
other_type_list = []
for name, obj in custom_module.__dict__.items():
    if inspect.isclass(obj):
        class_list.append(obj)
    elif inspect.isfunction(obj):
        function_list.append(obj)
    else:
        pass

# get instances
all_instances = []
for name, obj in custom_module.__dict__.items():
    if is_instance_from_langchain(type(obj), "langchain") and not isinstance(obj, type):
        all_instances.append(obj)


# load base flow template
base_class = get_base_class()
# generate the ids for vertexes

# create random position for the vertexes to show in the UI
position = allocate_components(len(all_instances))
function_list_copy = copy.copy(function_list)

for vertex, pos in zip(all_instances, position):
    # get the input variables from kwargs
    lc_kwargs = None
    try:
        if vertex._lc_kwargs:
            lc_kwargs = vertex._lc_kwargs
    except:
        pass

    # Chains
    if vertex.__module__.startswith("langchain.chains"):
        base_class['data']['nodes'].append(get_template("chains", vertex.__class__.__name__, vertex, pos,lc_kwargs))

    elif vertex.__module__.startswith("langchain.document_loaders"):
        base_class['data']['nodes'].append(get_template("documentloaders", vertex.__class__.__name__, vertex,pos,lc_kwargs))

    # Embeddings
    elif vertex.__module__.startswith("langchain.embeddings"):
        base_class['data']['nodes'].append(get_template("embeddings", vertex.__class__.__name__, vertex,pos,lc_kwargs))

    # LLms
    elif vertex.__module__.startswith("langchain.llms"):
        base_class['data']['nodes'].append(get_template("llms", vertex.__class__.__name__, vertex,pos,lc_kwargs))

    # Memories
    elif vertex.__module__.startswith("langchain.memory"):
        base_class['data']['nodes'].append(get_template("memories", vertex.__class__.__name__,vertex, pos,lc_kwargs))

    # Prompts
    elif vertex.__module__.startswith("langchain.prompts"):
        base_class['data']['nodes'].append(get_template("prompts", vertex.__class__.__name__,vertex, pos,lc_kwargs))

    # TextSplitters
    elif vertex.__module__.startswith("langchain.text_splitter"):
        base_class['data']['nodes'].append(get_template("textsplitters", vertex.__class__.__name__,vertex, pos,lc_kwargs))

    # ToolKits
    elif vertex.__module__.startswith("langchain.agents.agent_toolkits"):
        base_class['data']['nodes'].append(get_template("toolkits", vertex.__class__.__name__,vertex, pos,lc_kwargs))

    # Tools
    elif vertex.__module__.startswith("langchain.tools"):
        base_class['data']['nodes'].append(get_template("tools", vertex.__class__.__name__,vertex, pos,lc_kwargs))

    # Utilities
    elif vertex.__module__.startswith("langchain.utilities"):
        base_class['data']['nodes'].append(get_template("utilities", vertex.__class__.__name__,vertex, pos,lc_kwargs))

    # Vectors Stores
    elif vertex.__module__.startswith("langchain.vectorstores"):
        base_class['data']['nodes'].append(get_template("vectorstores", vertex.__class__.__name__,vertex, pos,lc_kwargs))

    # Wrappers
    elif vertex.__module__.startswith("langchain.requests"):
        base_class['data']['nodes'].append(get_template("wrappers", vertex.__class__.__name__,vertex, pos,lc_kwargs))

    # ZeroShotAgent
    elif vertex.__class__.__name__ == "ZeroShotAgent":
        base_class['data']['nodes'].append(get_template("agents", "ZeroShotAgent",vertex, pos,lc_kwargs))

    # AgentExecutor
    elif vertex.__class__.__name__ == "AgentExecutor":
        all_agents = dir(langchain.agents)
        for j in function_list:
            if j.__name__ in all_agents:
                func_name = j.__name__.split("_")
                func_name = "".join(func_name[1:])
                base_class['data']['nodes'].append(get_template("agents", func_name,vertex,pos,lc_kwargs))
                function_list.remove(j)
                break

    else:
        pass

# get the parent child for all the vertices
all_vertex_info_updated  = get_children(all_instances, function_list_copy)

# create the edges and update the base class
updated_base_class = create_edges(all_vertex_info_updated,base_class)

with open ('Converted_flows/converted_with_edges.json','w') as flow:
    json.dump(updated_base_class,flow, cls=SetEncoder)

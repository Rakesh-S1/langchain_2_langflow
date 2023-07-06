<<<<<<< HEAD
from typing import Any
import streamlit as st
from pprint import pprint

import json
import copy
import inspect
import langchain
import importlib.util
from langchain_to_langflow import (
    get_template,
    get_base_class,
    allocate_components,
    get_children,
    get_edge,
    get_vertex_agent_arg,
    get_vertex_arguments,
    is_instance_from_langchain,
    all_vertex_info,
)
=======
import inspect
import importlib.util
import json
import langchain
import copy
from vertex import (get_template, get_base_class,
                    allocate_components,
                    is_instance_from_langchain,
                    all_vertex_info)
>>>>>>> 4cb49b98955bd4f705ee0fa4850daa960faf5b4a

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
<<<<<<< HEAD
        if i._lc_kwargs: lc_kwargs = i._lc_kwargs
        elif i.lc_kwargs: lc_kwargs = i._lc_kwargs
        else:pass
    except:
        pass
    # Agents

    if i.__class__.__name__ == "ZeroShotAgent":
        base_class["data"]["nodes"].append(
            get_template("agents", "ZeroShotAgent", y, lc_kwargs, i)
        )
    if i.__class__.__name__ == "AgentExecutor":
=======
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
>>>>>>> 4cb49b98955bd4f705ee0fa4850daa960faf5b4a
        all_agents = dir(langchain.agents)
        for j in function_list:
            if j.__name__ in all_agents:
                func_name = j.__name__.split("_")
                func_name = "".join(func_name[1:])
                base_class['data']['nodes'].append(get_template("agents", func_name,vertex,pos,lc_kwargs))
                function_list.remove(j)
                break
<<<<<<< HEAD

    # Chains
    if i.__module__.startswith("langchain.chains"):
        base_class["data"]["nodes"].append(
            get_template("chains", i.__class__.__name__, y, lc_kwargs, i)
        )

    # Loaders

    elif i.__module__.startswith("langchain.document_loaders"):
        base_class["data"]["nodes"].append(
            get_template("documentloaders", i.__class__.__name__, y, lc_kwargs, i)
        )

    # Embeddings
    elif i.__module__.startswith("langchain.embeddings"):
        base_class["data"]["nodes"].append(
            get_template("embeddings", i.__class__.__name__, y, lc_kwargs, i)
        )
    # LLms
    elif i.__module__.startswith("langchain.llms"):
        base_class["data"]["nodes"].append(
            get_template("llms", i.__class__.__name__, y, lc_kwargs, i)
        )
    # Memories
    elif i.__module__.startswith("langchain.memory"):
        base_class["data"]["nodes"].append(
            get_template("memories", i.__class__.__name__, y, lc_kwargs, i)
        )
    # Prompts
    elif i.__module__.startswith("langchain.prompts"):
        base_class["data"]["nodes"].append(
            get_template("prompts", i.__class__.__name__, y, lc_kwargs, i)
        )
    # TextSplitters
    elif i.__module__.startswith("langchain.text_splitter"):
        base_class["data"]["nodes"].append(
            get_template("textsplitters", i.__class__.__name__, y, lc_kwargs, i)
        )
    # ToolKits
    elif i.__module__.startswith("langchain.agents.agent_toolkits"):
        base_class["data"]["nodes"].append(
            get_template("toolkits", i.__class__.__name__, y, lc_kwargs, i)
        )
    # Tools
    elif i.__module__.startswith("langchain.tools"):
        base_class["data"]["nodes"].append(
            get_template("tools", i.__class__.__name__, y, lc_kwargs, i)
        )
    # Utilities
    elif i.__module__.startswith("langchain.utilities"):
        base_class["data"]["nodes"].append(
            get_template("utilities", i.__class__.__name__, y, lc_kwargs, i)
        )
    # Vectors Stores
    elif i.__module__.startswith("langchain.vectorstores"):
        base_class["data"]["nodes"].append(
            get_template("vectorstores", i.__class__.__name__, y, lc_kwargs, i)
        )
    # Wrappers
    elif i.__module__.startswith("langchain.requests"):
        base_class["data"]["nodes"].append(
            get_template("wrappers", i.__class__.__name__, y, lc_kwargs, i)
        )
=======
>>>>>>> 4cb49b98955bd4f705ee0fa4850daa960faf5b4a

    else:
        pass

<<<<<<< HEAD
get_children(all_instances, function_list1)

for vertex in all_instances:
    if vertex.__class__.__name__ == "AgentExecutor":
        get_vertex_agent_arg(vertex, all_instances, function_list1)
    else:
        get_vertex_arguments(vertex, all_instances)
edges = get_edge(all_vertex_info)
base_class["data"]["edges"] = edges
# pprint(all_vertex_info, sort_dicts=False)
# for i in all_instances:
#     class_annotations = i.__annotations__


# # Print the argument names and type names
#     for arg_name, arg_type in class_annotations.items():
#         print(f"{arg_name} | Type: {arg_type}")
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
=======
# get the parent child for all the vertices
all_vertex_info_updated  = get_children(all_instances, function_list_copy)
>>>>>>> 4cb49b98955bd4f705ee0fa4850daa960faf5b4a

# create the edges and update the base class
updated_base_class = create_edges(all_vertex_info_updated,base_class)

<<<<<<< HEAD
with open("converted.json", "w") as flow:
    json.dump(base_class, flow, cls=SetEncoder)

# pprint(base_class, sort_dicts=False)
=======
with open ('Converted_flows/converted_with_edges.json','w') as flow:
    json.dump(updated_base_class,flow, cls=SetEncoder)
>>>>>>> 4cb49b98955bd4f705ee0fa4850daa960faf5b4a

import inspect
import importlib.util
import json
from typing import Any
import langchain
from get_vertexes import is_instance_from_langchain
from temp import get_template, get_base_class, allocate_components
from pprint import pprint
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

# base json
base_class = get_base_class()
postion = allocate_components(len(all_instances))
for i, y in zip(all_instances, postion):
    lc_kwargs = None
    try:
        if i._lc_kwargs:
            lc_kwargs = i._lc_kwargs
    except: pass
    # Agents
    # print(postion[all_instances.index(i)])
    if i.__class__.__name__ == "ZeroShotAgent":
        base_class['data']['nodes'].append(get_template("agents", "ZeroShotAgent",y, lc_kwargs))
    if i.__class__.__name__ == "AgentExecutor":
        all_agents = dir(langchain.agents)
        for j in function_list:
            if j.__name__ in all_agents:
                func_name = j.__name__.split("_")
                func_name = "".join(func_name[1:])
                base_class['data']['nodes'].append(get_template("agents", func_name, y, lc_kwargs))
                function_list.remove(j)
                break
                # continue
                # agents(j.__name__)
                # new_agent(i.__class__.__name__)

    # Chains
    if i.__module__.startswith("langchain.chains"):
        base_class['data']['nodes'].append(get_template("chains", i.__class__.__name__,y, lc_kwargs))

        # if False: base_class['data']['nodes'].append(get_template('chains','ZeroShotAgent')
    # Loaders

    elif i.__module__.startswith("langchain.document_loaders"):
        base_class['data']['nodes'].append(get_template("documentloaders", i.__class__.__name__,y, lc_kwargs))
        # print(i.__module__, inspect.getfile(i.__class__,y, lc_kwargs))
        # if False: base_class['data']['nodes'].append(get_template('documentloaders','ZeroShotAgent')
    # Embeddings
    elif i.__module__.startswith("langchain.embeddings"):
        base_class['data']['nodes'].append(get_template("embeddings", i.__class__.__name__,y, lc_kwargs))
    #     print(i.__class__)
    # if False: base_class['data']['nodes'].append(get_template('embeddings',i.__class__.__name__)
    # LLms
    elif i.__module__.startswith("langchain.llms"):
        base_class['data']['nodes'].append(get_template("llms", i.__class__.__name__,y, lc_kwargs))
        # if False: base_class['data']['nodes'].append(get_template('llms',i.__class__.__name__)
    # Memories
    elif i.__module__.startswith("langchain.memory"):
        base_class['data']['nodes'].append(get_template("memories", i.__class__.__name__,y, lc_kwargs))
        # if False: base_class['data']['nodes'].append(get_template('memories',i.__class__.__name__)
    # Prompts
    elif i.__module__.startswith("langchain.prompts"):
        base_class['data']['nodes'].append(get_template("prompts", i.__class__.__name__,y, lc_kwargs))
        # if False: base_class['data']['nodes'].append(get_template('prompts',i.__class__.__name__)
    # TextSplitters
    elif i.__module__.startswith("langchain.text_splitter"):
        base_class['data']['nodes'].append(get_template("textsplitters", i.__class__.__name__,y, lc_kwargs))
        # if False: base_class['data']['nodes'].append(get_template('textsplitters',i.__class__.__name__)
    # ToolKits
    elif i.__module__.startswith("langchain.agents.agent_toolkits"):
        base_class['data']['nodes'].append(get_template("toolkits", i.__class__.__name__,y, lc_kwargs))
        # if False: base_class['data']['nodes'].append(get_template('toolkits',i.__class__.__name__)
    # Tools
    elif i.__module__.startswith("langchain.tools"):
        base_class['data']['nodes'].append(get_template("tools", i.__class__.__name__,y, lc_kwargs))
        # if False: base_class['data']['nodes'].append(get_template('tools',i.__class__.__name__)
    # Utilities
    elif i.__module__.startswith("langchain.utilities"):
        base_class['data']['nodes'].append(get_template("utilities", i.__class__.__name__,y, lc_kwargs))
        # if False: base_class['data']['nodes'].append(get_template('utilities',i.__class__.__name__)
    # Vectors Stores
    elif i.__module__.startswith("langchain.vectorstores"):
        base_class['data']['nodes'].append(get_template("vectorstores", i.__class__.__name__,y, lc_kwargs))
        # if False: base_class['data']['nodes'].append(get_template('vectorstores',i.__class__.__name__)
    # Wrappers
    elif i.__module__.startswith("langchain.requests"):
        base_class['data']['nodes'].append(get_template("wrappers", i.__class__.__name__,y, lc_kwargs))
        # if False: base_class['data']['nodes'].append(get_template('wrappers',i.__class__.__name__)

    else:
        pass

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

with open ('converted.json','w') as flow:
    json.dump(base_class,flow, cls=SetEncoder) 

# pprint(base_class, sort_dicts=False)
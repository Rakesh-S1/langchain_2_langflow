from inspect import signature
from vertex import all_vertex_info
from langflow.utils.util import get_base_classes
import langchain
from langchain.agents import *

def get_vertex_data(vertex):
    # print(vertex)
    # print(vertex[1].__class__.__name__)
    for key, val in all_vertex_info.items():
        try:
            if val['vertex'] == vertex:
                return key
        except:
            if val['vertex'] is vertex:
                return key


def get_function_arg_type(function, all_instance) -> list:
    edge_update = {}
    edge = []
    function_name = function.__name__
    func = globals()[function_name]
    sig = signature(func)
    arguments_type = [(arg.name, arg.annotation) for arg in sig.parameters.values()]
    for i in all_instance:
        base_class = get_base_classes(i.__class__)
        for arg_name, arg_type in arguments_type:
            if arg_type.__name__ in base_class:
                edge.append(get_vertex_data(i))
    return edge


def get_children(vertices, function_list=None):
    for vertex in vertices:
        if vertex.__class__.__name__ == "AgentExecutor":
            all_agents = dir(langchain.agents)
            for j in function_list:
                if j.__name__ in all_agents:
                    parent_id = get_vertex_data(vertex)
                    children = get_function_arg_type(j, vertices)
                    if isinstance(children, list):
                        all_vertex_info[parent_id]['children'].extend(children)
                    else:
                        all_vertex_info[parent_id]['children'].append(children)
        else:
            for child in vertex:

                try:
                    if child[1] in vertices:
                        parent_id = get_vertex_data(vertex)
                        all_vertex_info[get_vertex_data(vertex)]['children'].append(get_vertex_data(child[1]))

                except:
                    pass
    return all_vertex_info



def create_edges(allinfo, base_class):
    for target_id, info_dict in allinfo.items():
        for source_id in info_dict['children']:

            edgebase = {}
            s_info = allinfo[source_id]
            edgebase['source'] = source_id
            edgebase['sourceHandle'] = "|".join([s_info['vertex_name'],source_id]+s_info['base_class'])
            edgebase['target'] = target_id
            edgebase['targetHandle'] = "|".join(s_info['base_class']+[s_info['component_name'],target_id])
            edgebase['style']= {"stroke": "inherit"},
            edgebase['className'] = "stroke-gray-900 dark:stroke-gray-200"
            edgebase['animated'] = False,
            edgebase['id'] = "reactflow_edge-"+edgebase['source']+"-"+edgebase['sourceHandle']+"-"+edgebase['target']+"-"+edgebase['targetHandle']
            # update the base_class
            base_class['data']['edges'].append(edgebase)
    return base_class



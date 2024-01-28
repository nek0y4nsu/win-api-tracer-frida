import os
import json
from graphviz import Digraph

def load_json(path):
    f = open(path,"r")
    text = f.read()
    f.close()
    return json.loads(text)
    
def gen_graph(label_list:list):
    dot=Digraph(comment='graph',filename='GraphTraceApi',format='jpg')
    
    for i in range(0,len(label_list)):
        dot.node(str(i), shape='box', style='filled',label=label_list[i],fontname='Microsoft YaHei')
        dot.edge(str(i),str(i+1))
    dot.view()


def show_trace_graph(log_path:str):
    print("show_trace_graph")
    
    log_list = load_json(log_path) 
    graph_label_list = []
    for x in log_list:
        if 'api_name' not in x:
            continue
        
        api_name = x['api_name']
        args_dict = x['content']
        
        content_v = "API NAME: %s \n" % api_name
        ### all arguements
        for p,t in args_dict.items():
            content_v += "     %s => %s \n" % (p,t)
        if 'dump' in x:
            content_v += "     dump => %s" % x['dump']
        
        graph_label_list.append(content_v)
        
    gen_graph(graph_label_list)
    
if __name__ == "__main__":
    print("Graph Trace")
import frida
import sys
import os
import time
import json
import show_graph
import argparse

log_list = []
verbose_flag = 0

def exportJsonLog(obj,path:str): 
    log = json.dumps(obj)
    f = open(path,'w')
    f.write(log)
    f.close()
    print("export json ok.")
    
    
def read_script(path):
    try:
        f = open(path,"r")
        content = f.read()
    except BaseException as e:
        print("read script failed,path: %s" % path)
        return ""
    finally:
        f.close()
    
    return content

def ExecuteProgram(path,arg=''):
    pid = frida.spawn(path)
    session = frida.attach(pid)
    print("PID: {}".format(pid))
    return (session,pid)
    
def on_message(message, data):
    global log_list
    global verbose_flag
    
    if message['type'] == 'send':
        payload = message['payload']
        log_list.append(payload)
        if verbose_flag == 1:
            print(payload)
        
        
def load_js_script(session):
    script_folder = "./apis_js/"
    script_list = []
    
    listdir = os.listdir(script_folder)
    for name in listdir:
        full_path = os.path.join(script_folder, name)
        script_list.append(full_path)
        
    print(script_list)
    
    for path in script_list:     
        script = session.create_script(read_script(path))
        script.on('message', on_message)
        script.load()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path",help="executable path")
    parser.add_argument("--second",help="wait seconds")
    parser.add_argument("--verbose",help="show verbose")
    args = parser.parse_args()
    
    if args.path and args.second:
        print("run:%s " % args.path)
    else:
        print("error")
        os._exit(0)
        
    if args.verbose:
        verbose_flag = 1
        print("[!]show verbose")
        
        
     
    s,pid = ExecuteProgram(args.path)
    load_js_script(s)
    
    print("---------------resume process---------------------")
    frida.resume(pid)
    
    print("wait   %s s....." % args.second)
    time.sleep(int(args.second))
    
    print("[!]Trace finished")
    print("stop process...")
    frida.kill(pid)
    print("[+]Export log (json)")
    exportJsonLog(log_list,"log.json")
    
    ###show graph
    show_graph.show_trace_graph("log.json")
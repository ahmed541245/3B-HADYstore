import json
import os

#? getting data func in json
def get_json_data (path):
    with open (path + ".json", "r") as file:
        return json.load (file)

#? updating data func in json
def updata_data (path, data):
    with open (path + ".json", "w") as file:
        json.dump (data, path, indent= 4)
    

def data_selector (obj):
    if type (obj) == str:
        return get_json_data (obj)
    elif type (obj) == dict :
        return obj
    assert type (obj) in [str, dict], "The type is invaled, you should put a json data or json file path"
    

#? checking obj foundation func in json
def check_obj (path, listname, attr_name, value):
    data = data_selector (path)
    lst = data [listname]
    for obj in lst :
        if obj [attr_name] == value:
            return True
        else : found = False
    return found

#? checking value foundation func in json
def check_value (path, listname, value):
    data = data_selector (path)
    lst = data [listname]
    return value in lst

#? get object from var
def get_obj (path, listname, varname, value):
    data = data_selector (path)
    lst = data [listname]
    for obj in lst :
        if obj [varname] == value:
            return obj
        else : found = False
    return found


#? json files management decorator
def manage_files (func):
    def wrapper (path, *args, **kwargs) :
        data = get_json_data (path)
        final_data = func (data, *args, **kwargs)
        updata_data (path, final_data)
    return wrapper

#? adding vlaue to a list func in json
@manage_files
def add_obj2list (path, listname, obj):
    data = path
    lst = list (data [listname])
    lst.append (obj)
    return data

#? removing value from a list func in json
@manage_files
def remove_obj_from_list (path, listname, obj):
    data = path
    lst = list (data [listname])
    lst.remove (obj)
    return data

#? adding vareble to all objects in the list func in json
@manage_files
def add_var2all_objs (path, listname, varname, defcult_value):
    data = path
    lst = list (data [listname])
    for obj in lst :
        obj [varname] = defcult_value
    return data

#? removing vareble to all objects in the list func in json
@manage_files
def add_var2all_objs (path, listname, varname):
    data = path
    lst = list (data [listname])
    for obj in lst :
        obj = dict (obj)
        obj.pop (varname)
    return data

#? updating object's value func in json
@manage_files
def update_value (path, listname, var_sellector_name, sellector_value, var_name, value):
    data = path
    lst: list = data [listname]
    obj : dict = get_obj (data, listname, var_sellector_name, sellector_value)
    if obj == False : return False
    new_obj = obj.copy () 
    new_obj [var_name] = value
    lst.remove (obj)
    list.append (new_obj)
    return data
    
#? updating all objects's value func in json
def update_all_values (path, listname, var_name, value):
    data = path
    lst = data [listname]
    for obj in lst :
        obj [var_name] = value
    return data

#? creating json file
def creat_json_file (path, data):
    with open (path + ".json", "w") as file:
        json.dump (data, file, indent= 4)

#? remove any file
def remove_file (path):
    os.remove (path)
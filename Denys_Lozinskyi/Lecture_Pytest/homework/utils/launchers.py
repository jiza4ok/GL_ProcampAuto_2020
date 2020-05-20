import os
import signal
import requests
from subprocess import Popen
from datetime import datetime
from urllib.parse import urljoin
from ..config import *


def start_server(link_to_server: str, timeout=5) -> Popen:
    """ Runs the server locally placed in the system.
        Tries to fulfill the task within the time in seconds passed as the timeout parameter.
        If the run successful - returns the server process as a subprocess.Popen object.
        Kills the process and raises an exception otherwise
        :param link_to_server: a local system link to the server.
        :param timeout: time in seconds for attempts to start the server
        :return :process as subprocess.Popen object
    """
    terminal_command = f"python3 {link_to_server}"
    server_process = Popen(terminal_command, shell=True, preexec_fn=os.setsid)
    time_start = datetime.now()
    while (datetime.now() - time_start).seconds < timeout:
        try:
            response = requests.get(urljoin(base_url, root_endpoint))
            response.raise_for_status()
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
            continue
        else:
            break
    else:
        os.killpg(server_process.pid, signal.SIGTERM)
        raise Exception('Server is not responding')
    return server_process


def stop_server(server_process: Popen):
    """ Stops the server process passed as an argument
        :param server_process: subprocess.Popen object
    """
    os.killpg(server_process.pid, signal.SIGTERM)

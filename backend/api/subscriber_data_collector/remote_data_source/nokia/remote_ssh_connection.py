import asyncio
import logging
from paramiko import SSHClient, AutoAddPolicy
import re

from .exceptions import CentralConnectionException
from ...entities.network_element import NetworkElement

logging.getLogger().setLevel(logging.INFO)


class RemoteSshConnectionImpl():

    def __init__(
            self,
            timeout: float = 5,
            endline_char='\r'
    ):
        self.timeout = timeout
        self.endline_char = endline_char
        self.ssh_client = SSHClient()
        # util.log_to_file(log_filename)

    async def set_client(self, network_element: NetworkElement):
        self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        try:
            self.ssh_client.connect(
                hostname=network_element.hostname,
                port=network_element.port,
                timeout=self.timeout,
                username=network_element.username,
                password=network_element.password)
        except Exception as e:
            logging.error(f'Connection element {network_element.name} {e}')
            raise CentralConnectionException(e)

        self.socket = self.ssh_client.invoke_shell()
        await asyncio.sleep(5)

    async def send(self, command):
        self.socket.send(command + self.endline_char)
        await asyncio.sleep(10)

    async def receive(self, length, key='COMMAND EXECUTED') -> str:
        output = ""
        loop = asyncio.get_running_loop()
        while True:
            logging.info("looping data of mss")
            data = str(await loop.run_in_executor(None, self.socket.recv, length),
                    encoding='utf-8', errors='ignore')
            logging.info(data)
            output += data
            if(re.search(r"{}".format(key), output)):
                break
        return output

    def close(self):
        self.ssh_client.close()

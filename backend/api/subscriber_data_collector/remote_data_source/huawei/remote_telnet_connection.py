import logging
import socket
import asyncio
import re

from subscriber_data_collector.remote_data_source.huawei.ossConnectionException import OssConnectionException
from subscriber_data_collector.constants import RemoteDataSourceConstants


class TelnetShellImpl():
    """Implementation of a telnet connection to a network element"""

    def __init__(self):
        self.socket = None

    async def set_connection(self, oss):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((oss.hostname, oss.port))
            await self.send("LGI:OP={}, PWD={};".format(oss.user_name, oss.password))
            output = await self.recv(lenght=10000)
            if not self.check_success_logging(output):
                logging.info(f"Oss failed to logging error: {output}")
                raise OssConnectionException(OssConnectionException)
            logging.info("Oss connection established")
        except Exception as e:
            logging.error(f"{RemoteDataSourceConstants.SOCKET_ERROR}{e}")
            raise OssConnectionException(e)

    def check_success_logging(self, text):
        # Define and search for the regex pattern in one line
        return bool(re.search(r"Success\b", text))

    async def send(self, command, time=3):
        if self.socket is None:
            logging.error(
                "Socket is none, connection with oss was not established or have problems"
            )
            return
        self.socket.sendall((command + "\r\n").encode(encoding="utf-8"))
        await asyncio.sleep(time)

    async def recv(self, lenght) -> str:
        if self.socket is None:
            logging.error(
                "Socket is none, connection with oss was not established or have problems"
            )
            raise OssConnectionException(error="Connection lost while receiving data")
        logging.info("getting data")
        output = ""
        data = str(self.socket.recv(lenght), encoding="utf-8", errors="ignore")
        output = data
        logging.info("Data received")
        return output

    async def close(self):
        if self.socket is not None:
            self.socket.close()

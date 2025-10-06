import logging

from .remote_telnet_connection import TelnetShellImpl
from .ossConnectionException import OssConnectionException
from ...constants import RegexPatterns
import re


class RemoteOssConnection:

    def __init__(self, telnet_shell: TelnetShellImpl):
        """Initialize the remote oss connection with a telnet shell and a network element"""

        self._oss_connection = telnet_shell

    async def set_connection(self, oss):
        await self._oss_connection.set_connection(oss)

    async def connect_to_network_element(self, network_element):

        await self._oss_connection.send(f"REG NE:NAME={network_element.name};")
        output = await self._oss_connection.recv(200000)
        if self._check_ne_connection(output):
            logging.info(f"Successfully connected to {network_element.name}")
        else:
            await self._oss_connection.close()
            logging.error(
                f"Failed to connect to ne {network_element.name}: /n {output}")

            raise OssConnectionException(
                f"Failed to connect to ne {network_element.name}")
        return output

    async def _connect_to_vnfc(self, network_element):
        await self._oss_connection.send(f"REG VNFC:NAME={network_element.vnfc_name};")
        output = await self._oss_connection.recv(200000)
        if self._check_vnfc_connection(output):
            logging.info(f"Successfully connected to {network_element.vnfc_name}")
        else:
            await self._oss_connection.close()
            logging.error(
                f"Failed to connect to vnfc {network_element.vnfc_name}: /n {output}")

            raise OssConnectionException(
                f"Failed to connect to vnfc {network_element.vnfc_name}")

    async def get_output(self, command) -> str:
        await self._oss_connection.send(command)
        return await self._oss_connection.recv(500000)

    async def close_oss_connection(self, network_element):
        logging.info("closing connection to vnfc")
        await self._oss_connection.send(f"UNREG VNFC:NAME={network_element.vnfc_name};")
        logging.info("closing connection to ne")
        await self._oss_connection.send(f"UNREG NE:NAME={network_element.vnfc_name};")
        logging.info("closing connection to oss")
        await self._oss_connection.close()

    def _check_ne_connection(self, output):
        return re.search(
            RegexPatterns.CHECK_CONNECTION,
            output,
            flags=re.MULTILINE)

    def _check_vnfc_connection(self, output):
        return re.search(
            RegexPatterns.CHECK_VNFC_CONNECTION,
            string=output,
            flags=re.MULTILINE
        )
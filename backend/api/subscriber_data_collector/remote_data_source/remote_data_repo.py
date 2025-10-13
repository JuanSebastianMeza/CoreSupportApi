import asyncio
import logging
import re

from ..entities.output_logs import OutputLogs
from ..entities.oss import Oss
from ..entities.network_element import NetworkElement
from ..entities.subscriber import Subscriber

from .huawei.remote_oss_connection import RemoteOssConnection
from .nokia.remote_ssh_connection import RemoteSshConnectionImpl
from .nokia.remote_centrals import Centrales_Nokia_List

from ..constants import HuaweiCommands, NokiaCommands, RegexPatterns, OutputMessages

logging.getLogger().setLevel(level=logging.INFO)


class RemoteDataRepo:

    def __init__(
        self,
        oss_connection: RemoteOssConnection,
        ssh_connection: RemoteSshConnectionImpl,
    ) -> None:
        self._oss_connection = oss_connection
        self._ssh_connection = ssh_connection

    async def _gets_output(self, command) -> str:
        logging.info(f"Sending command: {command}")
        return await self._oss_connection.get_output(command)

    async def get_mmctx(self, msisdn):
        # Connection set up
        list_of_sgsn = ["vSGSNCAN01", "vSGSNCOL01", "SGSNVAL01", "SGSNMCY02"]
        try:
            for sgsn in list_of_sgsn:
                logging.info(f"Connecting to {sgsn}")
                await self._oss_connection.set_connection(oss=Oss())
                current_ne = NetworkElement(name=f"{sgsn}", vnfc_name="omo")
                await self._oss_connection.connect_to_network_element(current_ne)
                if sgsn in ["vSGSNCAN01", "vSGSNCOL01"]:
                    await self._oss_connection._connect_to_vnfc(current_ne)
                # Send command to get MMCTX data
                output = await self._gets_output(
                    command=HuaweiCommands.DSP_MMCTX_MSISDN.format(msisdn)
                )
                # Check if the output contains the expected pattern
                if self._check_mmctx_not_found(output) is False:
                    logging.info(f"MMCTX data for {msisdn} is in {sgsn}: {output}")
                    await self._oss_connection.close_oss_connection(current_ne)
                    return Subscriber(
                        msisdn=msisdn,
                        imsi=re.findall(RegexPatterns.IMSI, output)[0],
                        vlr=re.findall(RegexPatterns.VLR, output)[0],
                        sgsn=sgsn,
                        output_logs=OutputLogs(
                            mmctx=output
                        ),
                        last_activity_paco=re.findall(
                            RegexPatterns.ACTIVITY_TIME_PACO, output
                        )[0],
                    )
                logging.error(f"Failed to get MMCTX data for {msisdn} in {sgsn}: {output}")
                await self._oss_connection.close_oss_connection(current_ne)
        except Exception as e:
            logging.info(OutputMessages.MMCTX_ERROR + f" SGSN: {sgsn} Error: {e}")
            return Subscriber(msisdn=msisdn,sgsn=sgsn, output_logs=OutputLogs(mmctx=OutputMessages.MMCTX_ERROR + f" SGSN: {sgsn} Error: {e}"))
        return Subscriber(msisdn=msisdn, sgsn=sgsn, output_logs=OutputLogs(mmctx=OutputMessages.MMCTX_NOT_FOUND))

    def _check_mmctx_not_found(self, output):
        # Check if the output contains the expected pattern
        return bool(re.search(r"Record does not exist.", output))

    async def get_s1aplnk_4g(self, enodeB_id, sgsn_name):
        # Connection set up
        try:
            logging.info(f"Connecting to {sgsn_name}")
            await self._oss_connection.set_connection(oss=Oss())
            current_ne = NetworkElement(name=f"{sgsn_name}", vnfc_name="omo")
            await self._oss_connection.connect_to_network_element(current_ne)
            if sgsn_name in ["vSGSNCAN01", "vSGSNCOL01"]:
                await self._oss_connection._connect_to_vnfc(current_ne)
            # Send command to get S1APLN data
            output = await self._gets_output(
                command=HuaweiCommands.DSP_S1APLNK.format(enodeB_id)
            )
            # Check if the output contains the expected pattern
            if self._check_s1aplnk(output) is False:
                logging.error(
                    f"Failed to get S1APLN data for {enodeB_id} in {sgsn_name}: {output}"
                )
                await self._oss_connection.close_oss_connection(current_ne)
                return f"enodeB is not registered in any SGSN {sgsn_name}"
            logging.info(f"S1APLN data for {enodeB_id} is in {sgsn_name}: {output}")
            await self._oss_connection.close_oss_connection(current_ne)
        except Exception as e:
            logging.info(OutputMessages.S1APLNK_ERROR + f" {e}")
            return OutputMessages.S1APLNK_ERROR + f" {e}"
        return output

    def _check_s1aplnk(self, output):
        return bool(re.search(RegexPatterns.CHECK_S1APLNK, output))

    async def get_zepo_output(self, access_id, gsm: bool):
        for central in Centrales_Nokia_List:
            logging.info(f"Connecting to {central}")
            try:
                await self._ssh_connection.set_client(central)
                if gsm:
                    await self._ssh_connection.send(NokiaCommands.ZEPO_2G.format(access_id))
                else:
                    await self._ssh_connection.send(NokiaCommands.ZEPO_3G.format(access_id))

                task_getting_data = asyncio.create_task(
                self._ssh_connection.receive(100000)
                )
                output = await asyncio.wait_for(task_getting_data, 10)
                if self.check_zepo_output(output) is False:
                    return output
            except asyncio.TimeoutError as e:
                logging.error(
                    OutputMessages.TIMER_ERROR_MSS + f" {e}"
                )
                task_getting_data.cancel()
                return OutputMessages.TIMER_ERROR_MSS + f" {e}"
            except Exception as e:
                logging.error(
                    f"Problems gathering ZEPO data. Error: {e}"
                )
                return OutputMessages.ZEPO_ERROR_MSS + f" {e}"


    def check_zepo_output(self, output):
        # Check if the output contains the expected pattern
        return bool(re.search(RegexPatterns.CHECK_ZEPO, output))

    async def get_zmvo_output(self, msisdn: str):
        for central in Centrales_Nokia_List:
            logging.info(f"Getting zmvo data. Connecting to {central}")
            try:
                await self._ssh_connection.set_client(central)
                await self._ssh_connection.send(NokiaCommands.ZMVO.format(msisdn))
                task_getting_data = asyncio.create_task(
                self._ssh_connection.receive(100000)
            )
                output = await asyncio.wait_for(task_getting_data, 10)
                if self._check_zmvo_output(output) is False:
                    return [output, central.name]
            except asyncio.TimeoutError as e:
                logging.error(
                    OutputMessages.TIMER_ERROR_MSS + f" {e}"
                )
                task_getting_data.cancel()
                return [OutputMessages.TIMER_ERROR_MSS + f" {e}"]
            except Exception as e:
                logging.error(
                    f"Problems gathering ZEPO data. Error: {e}"
                )
                return [OutputMessages.ZMVO_ERROR_MSS + f" {e}"]


    def _check_zmvo_output(self, output):
        # Check if the output contains the expected pattern
        return bool(re.search(RegexPatterns.CHECK_ZMVO, output))


    async def get_uppdpchginfo(self, msisdn):
        # Connection set up
        list_of_vsgsn = ["vGGSNCAN_DGW_01", "vGGSNMCY_DGW_01"]
        try:
            for vggsn in list_of_vsgsn:
                logging.info(f"Connecting to {vggsn}")
                await self._oss_connection.set_connection(oss=Oss())
                current_ne = NetworkElement(name=f"{vggsn}", vnfc_name="dgw")
                await self._oss_connection.connect_to_network_element(current_ne)
                await self._oss_connection._connect_to_vnfc(current_ne)
                # Send command to get MMCTX data
                output = await self._gets_output(
                    command=HuaweiCommands.DSP_UPPDPCHGINFO.format(msisdn)
                )
                # Check if the output contains the expected pattern
                if self._check_mmctx_not_found(output) is False:
                    logging.info(f"MMCTX data for {msisdn} is in {vggsn}: {output}")
                    await self._oss_connection.close_oss_connection(current_ne)
                    return Subscriber(
                        msisdn=msisdn,
                        imsi=re.findall(RegexPatterns.IMSI, output)[0],
                        sgsn=vggsn,
                        output_logs=OutputLogs(
                            mmctx=output
                        ),
                        last_activity_paco=re.findall(
                            RegexPatterns.ACTIVITY_TIME_PACO, output
                        )[0],
                    )
                logging.error(f"Failed to get MMCTX data for {msisdn} in {vggsn}: {output}")
                await self._oss_connection.close_oss_connection(current_ne)
        except Exception as e:
            logging.info(OutputMessages.MMCTX_ERROR + f" SGSN: {vggsn} Error: {e}")
            return Subscriber(msisdn=msisdn,sgsn=vggsn, output_logs=OutputLogs(mmctx=OutputMessages.MMCTX_ERROR + f" SGSN: {vggsn} Error: {e}"))
        return Subscriber(msisdn=msisdn, sgsn=vggsn, output_logs=OutputLogs(mmctx=OutputMessages.MMCTX_NOT_FOUND))

    def _check_uppdpchginfo_not_found(self, output):
        # Check if the output contains the expected pattern
        return bool(re.search(r"Record does not exist.", output))
import logging
import re

from .entities.cell import Cell
from .entities.enodeB import EnodeB
from .entities.network import Network
from .entities.nodeB import NodeB
from .entities.subscriber import Subscriber
from .networks import Networks
from .constants import OutputMessages, RegexPatterns
from .remote_data_source.remote_data_repo import RemoteDataRepo

logging.getLogger().setLevel(level=logging.INFO)


class CheckSubscriberData:
    """
    Class to check subscriber data and get the network information.
     - Pending cases:
        - When subscriber is unregister and out of service
    """

    def __init__(
        self,
        remote_repo: RemoteDataRepo,
    ):
        self._remote_repo = remote_repo

    async def check_subscriber(self, current_subscriber: Subscriber):
        try:
            current_subscriber = await self._remote_repo.get_mmctx(
                current_subscriber.msisdn
            )  # type: ignore
            access_data = self.get_access_data(current_subscriber.output_logs.mmctx)
            # TODO: check if the subscriber is unregister in all sgsn

            current_subscriber.network = access_data

            if current_subscriber.network.technology == Networks.LTE.name:
                s1aplnk_output = await self._remote_repo.get_s1aplnk_4g(
                    current_subscriber.network.enodeb.enodeb_id, current_subscriber.sgsn
                )
                current_subscriber.output_logs.s1aplnk = s1aplnk_output
                current_subscriber.network.enodeb.name = re.findall(
                    RegexPatterns.ENODEB_NAME, s1aplnk_output
                )[0]
                current_subscriber.network.enodeb.link_status = re.findall(
                    RegexPatterns.ENODEB_LINK_STATUS, s1aplnk_output
                )[0]
                current_subscriber.network.enodeb.ip_address1 = re.findall(
                    RegexPatterns.ENODEB_PRIMARY_IP, s1aplnk_output
                )[0]
                current_subscriber.network.enodeb.ip_address2 = re.findall(
                    RegexPatterns.ENODEB_SECONDARY_IP, s1aplnk_output
                )[0]
                current_subscriber.network.enodeb.port = int(
                    re.findall(RegexPatterns.ENODEB_PORT, s1aplnk_output)[0]
                )

            if current_subscriber.network.technology == Networks.UMTS.name:
                logging.info("getting data from mss")
                zepo_output = await self._remote_repo.get_zepo_output(
                    current_subscriber.network.nodeb.sa_id, False
                )
                if zepo_output:
                    current_subscriber.output_logs.zepo = zepo_output
                    current_subscriber.network.nodeb.lac_id = int(
                        re.findall(RegexPatterns.LAC_ID, zepo_output)[0]
                    )
                    current_subscriber.network.nodeb.sa_name = re.findall(
                        RegexPatterns.SA_NAME, zepo_output
                    )[0]
                    current_subscriber.network.nodeb.administrative_state = re.findall(
                        RegexPatterns.ADMINISTRATIVE_STATE, zepo_output
                    )[0]

            if current_subscriber.network.technology == Networks.GSM.name:
                logging.info("getting data from mss")
                zepo_output = await self._remote_repo.get_zepo_output(
                    current_subscriber.network.cell.bts_id, True
                )
                if zepo_output:
                    current_subscriber.output_logs.zepo = zepo_output
                    bts_data = re.findall(RegexPatterns.BTS_NAME_ID, zepo_output)
                    current_subscriber.network.cell.bts_name = bts_data[0][0]
                    current_subscriber.network.cell.bts_id = int(bts_data[0][1])
                    bsc_data = re.findall(RegexPatterns.BSC_NAME_ID, zepo_output)
                    current_subscriber.network.cell.bsc_name = bsc_data[0][0]
                    current_subscriber.network.cell.bsc_id = int(bsc_data[0][1])
                    current_subscriber.network.cell.bts_state = re.findall(
                        RegexPatterns.BTS_STATE, zepo_output
                    )[0]

            # Set the zepo data
            current_subscriber = await self.set_zmvo_data(current_subscriber)
            return current_subscriber
        except Exception as e:
            print(f"Error: {e}")
            return current_subscriber

    async def _get_enodeb_data(self, enodeb_id: int, sgsn: str):
        return await self._remote_repo.get_s1aplnk_4g(enodeb_id, sgsn)

    def get_access_data(self, mmctx_output: str):
        if bool(re.search(RegexPatterns.CHECK_MMCTX_FAILED, mmctx_output)):
            logging.info("mmctx data failed")
            return Network(OutputMessages.MMCTX_ERROR)

        if bool(re.findall(RegexPatterns.ENODEB_ID, mmctx_output)):
            decimal_enodeb_id = int(
                re.findall(RegexPatterns.ENODEB_ID, mmctx_output)[0], 16
            )
            logging.info("Subscriber is in 4G/LTE")
            return Network(
                technology=Networks.LTE.name, enodeb=EnodeB(enodeb_id=decimal_enodeb_id)
            )
        if bool(re.findall(RegexPatterns.SERVICE_AREA_ID, mmctx_output)):
            decimal_service_area = int(
                re.findall(RegexPatterns.SERVICE_AREA_ID, mmctx_output)[0], 16
            )
            logging.info(msg="Subscriber is in 3G/UMTS")

            return Network(
                technology=Networks.UMTS.name, nodeb=NodeB(sa_id=decimal_service_area)
            )
        if bool(re.findall(RegexPatterns.CELL_ID, mmctx_output)):
            decimal_cell_id = int(
                re.findall(RegexPatterns.CELL_ID, mmctx_output)[0], 16
            )
            logging.info(msg="Subscriber is in 2G/GSM")
            return Network(
                technology=Networks.GSM.name, cell=Cell(bts_id=decimal_cell_id)
            )
        return Network(technology=Networks.UNREGISTER.value)

    async def set_zmvo_data(self, subscriber: Subscriber) -> Subscriber:
        output = await self._remote_repo.get_zmvo_output(subscriber)
        if output:
            subscriber.output_logs.zmvo = output[0]
            subscriber.last_activity_cico = re.findall(
                RegexPatterns.ACTIVITY_DATE_CICO, output[0]
            )[0]
            subscriber.routing_category = re.findall(
                RegexPatterns.ROUTING_CATEGORY, output[0]
            )[0]
            subscriber.services = re.findall(RegexPatterns.SERVICES, output[0])[0]
            subscriber.mss = output[1]
        return subscriber

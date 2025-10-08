import asyncio
import logging

from rest_framework.response import Response

from .error_handler import BusinessLogicException
from rest_framework import status

from adrf.views import APIView

from .models import (
    NetworkModel,
    OutputLogsModel,
    SubscriberModel,
    EnodeBModel,
    NodeBModel,
    CellModel,
)
from .serializers import SubscriberSerializer

from .team_notifier.teams_notifier import send_teams_file, send_teams_notification
from .constants import OutputMessages
from .check_subscriber import CheckSubscriberData
from .remote_data_source.nokia.remote_ssh_connection import RemoteSshConnectionImpl
from .remote_data_source.remote_data_repo import RemoteDataRepo
from .remote_data_source.huawei.remote_oss_connection import RemoteOssConnection
from .remote_data_source.huawei.remote_telnet_connection import TelnetShellImpl

from .entities.subscriber import Subscriber

logging.getLogger().setLevel(level=logging.INFO)


# to run uvicorn api.asgi:application --reload
# GET /your-endpoint/?msisdn=123456789
# Create your views here.
class GetSubscribersData(APIView):
    async def get(self, request):
        msisdns = request.GET.get("msisdn")

        if not msisdns:
            logging.warning("msisdn is empty")
            return Response(
                {"error": "MSISDN parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        msisdn_list = [x.strip() for x in msisdns.split(",")]
        logging.info(f"MSISDNs: {msisdn_list}")

        # Check if the list of MSISDNs are in the correct format

        if not valid_msisdns_list(msisdn_list):
            return Response(
                {
                    "error": f"Invalid MSISDN format: {msisdn_list}, {OutputMessages.MSISDN_FORMAT_ERROR}",
                    "code": "invalid_msisdn_format",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            subscribers = [Subscriber(msisdn=msisdn) for msisdn in msisdn_list]
            tasks_list = [
                asyncio.create_task(run_csd(subscriber)) for subscriber in subscribers
            ]
            subscribers_data_list = []
            for task in tasks_list:
                subscribers_data_list.append(await asyncio.shield(task))
            # logging.info(f"subscriber_data_list: {subscribers_data_list}")
            subscriber_model_list = convert_subscribers_entity_to_model(subscribers_data_list)
            logging.info(f"Subscriber model list = {subscriber_model_list}")
            serializer = SubscriberSerializer(subscriber_model_list, many=True)
            logging.info(f"Subscriber serializer list = {serializer.data}")
            return Response(serializer.data, status=status.HTTP_200_OK)

        except BusinessLogicException as e:
            logging.error(f"Error in business logic: {e}")
            return Response(
                {"error": str(e), "code": e.default_code}, status=e.status_code
            )


# class GetSubscribersData(APIView):
#     async def get(self, request):
#         msisdns = request.GET.get("msisdn")

#         if not msisdns:
#             logging.warning("msisdn is empty")
#             return Response(
#                 {"error": "MSISDN parameter is required"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         msisdn_list = [x.strip() for x in msisdns.split(",")]
#         logging.info(f"MSISDNs: {msisdn_list}")

#         # Check if the list of MSISDNs are in the correct format

#         if not valid_msisdns_list(msisdn_list):
#             return Response(
#                 {
#                     "error": f"Invalid MSISDN format: {msisdn_list}, {OutputMessages.MSISDN_FORMAT_ERROR}",
#                     "code": "invalid_msisdn_format",
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         s_model = SubscriberModel(
#             msisdn="123456789",
#             imsi="987654321",
#             output_logs=OutputLogsModel(
#                 mmctx="mmctx log",
#                 s1aplnk="s1aplnk log",
#                 zepo="zepo log",
#                 zmvo="zmvo log",
#             ),
#             network=NetworkModel(
#                 technology="LTE",
#                 enodeb=EnodeBModel(
#                     name="eNodeB1",
#                     enodeb_id=1,
#                     link_status="connected",
#                     ip_address1="192.168.1.1",
#                     ip_address2="192.168.1.2",
#                     port=8080,
#                 ),
#                 cell=CellModel(
#                     bts_id=101,
#                     bts_name="Cell1",
#                     bts_state="active",
#                     bsc_name="BSC1",
#                     bsc_id=201,
#                 ),
#                 nodeb=NodeBModel(
#                     sa_name="NodeB1",
#                     sa_id=301,
#                     lac_id=401,
#                     administrative_state="unlocked",
#                 ),
#             ),
#         )
#         logging.info(f"Subscriber model: {s_model}")
#         subs_list = [s_model]
#         serializer = SubscriberSerializer(subs_list, many=True)
#         logging.info(f"Subscriber serializer: {serializer}")
#         data = serializer.data
#         logging.info(f"Subscriber serializer data: {data}")
#         return Response(data, status=status.HTTP_200_OK
#         )


async def run_csd(subscriber):
    # Dependencies initialization

    telnet_connection = TelnetShellImpl()
    oss_connection = RemoteOssConnection(telnet_connection)
    ssh_connection = RemoteSshConnectionImpl()
    remote_repo = RemoteDataRepo(oss_connection, ssh_connection)

    csd = CheckSubscriberData(remote_repo)
    subscriber = await csd.check_subscriber(subscriber)
    # notification = build_notification_message(subscriber)
    # try:
    #     logging.info("Sending team notification")
    #     send_teams_notification(notification)
    #     logging.info("Sending team log file notification")

    #     with open("log_file.log", "w") as f:
    #         f.write(f"""
    #     mmctx:
    #     {subscriber.output_logs.mmctx}
    #     s1aplnk:
    #     {subscriber.output_logs.s1aplnk}
    #     zmvo:
    #     {subscriber.output_logs.zmvo}
    #     zepo:
    #     {subscriber.output_logs.zepo}
    #                 """)

    #     send_teams_file("log_file.log")
    # except Exception as e:
    #     logging.error(f"Error trying to send teams notification: {e}")
    #     return subscriber

    return subscriber


def build_notification_message(subscriber):
    return f"""
<b>📱 Subscriber Information</b><br>
<hr>
<ul>
<li><b>MSISDN:</b> {subscriber.msisdn}</li>
<li><b>IMSI:</b> {subscriber.imsi}</li>
<li><b>SGSN:</b> {subscriber.sgsn}</li>
<li><b>MSS:</b> {subscriber.mss}</li>
<li><b>Routing Category:</b> {subscriber.routing_category}</li>
<li><b>Services:</b> {subscriber.services}</li>
</ul>

<b>🕒 Activity</b><br>
<hr>
<ul>
<li><b>Last Activity PACO:</b> {subscriber.last_activity_paco}</li>
<li><b>Last Activity CICO:</b> {subscriber.last_activity_cico}</li>
</ul>

<b>🌐 Network Technology:</b> {subscriber.network.technology}<br>
<hr>

<b>🚀 LTE Details</b><br>
<ul>
<li><b>EnodeB ID:</b> {subscriber.network.enodeb.enodeb_id}</li>
<li><b>EnodeB Name:</b> {subscriber.network.enodeb.name}</li>
<li><b>EnodeB IP:</b> {subscriber.network.enodeb.ip_address1}</li>
<li><b>EnodeB IP2:</b> {subscriber.network.enodeb.ip_address2}</li>
<li><b>EnodeB Port:</b> {subscriber.network.enodeb.port}</li>
<li><b>EnodeB Link Status:</b> {subscriber.network.enodeb.link_status}</li>
</ul>

<b>📡 UMTS Details</b><br>
<ul>
<li><b>NodeB Name:</b> {subscriber.network.nodeb.sa_name}</li>
<li><b>Service Area ID:</b> {subscriber.network.nodeb.sa_id}</li>
<li><b>LAC ID:</b> {subscriber.network.nodeb.lac_id}</li>
<li><b>State:</b> {subscriber.network.nodeb.administrative_state}</li>
</ul>

<b>📶 GSM Details</b><br>
<ul>
<li><b>Cell ID:</b> {subscriber.network.cell.bts_id}</li>
<li><b>Cell Name:</b> {subscriber.network.cell.bts_name}</li>
<li><b>Cell State:</b> {subscriber.network.cell.bts_state}</li>
<li><b>BSC Name:</b> {subscriber.network.cell.bsc_name}</li>
<li><b>BSC ID:</b> {subscriber.network.cell.bsc_id}</li>
</ul>
"""


def valid_msisdns_list(msisdn_list):
    """Check if the list of MSISDNs are in the correct format.
    The MSISDN should be max 15 digits long and contain only digits.
    The first 3 digits are the country code (CC), the next 3 digits are the
    subscriber number (SN), and the last 6 digits are the national destination code (NDC).

    CC + NDC + SN

    Country code (CC)
    National Destination Code (NDC)
    Subscriber number (SN)

    Examples:

    CC: 34 (Spain)
    NDC: 123 (Madrid)
    SN: 4567890 (subscriber number)

    CC: 58 (Venezuela)
    NDC: 414 (Caracas)
    SN: 1234567 (subscriber number)
    """
    for msisdn in msisdn_list:
        if len(msisdn) > 15:
            return False
        if not msisdn.isdigit():
            return False
        if len(msisdn) < 5:
            return False
    return True


def convert_subscribers_entity_to_model(
    subscribers: list[Subscriber],
) -> list[SubscriberModel]:
    """Convert a list of Subscriber objects to a list of SubscriberModel objects."""
    model_list = []

    for subscriber in subscribers:
        subscriber = SubscriberModel(
            imsi=subscriber.imsi,
            msisdn=subscriber.msisdn,
            sgsn=subscriber.sgsn,
            mss=subscriber.mss,
            last_activity_cico=subscriber.last_activity_cico,
            last_activity_paco=subscriber.last_activity_paco,
            routing_category=subscriber.routing_category,
            services=subscriber.services,
            output_logs=OutputLogsModel(
                mmctx=subscriber.output_logs.mmctx,
                zepo=subscriber.output_logs.zepo,
                s1aplnk=subscriber.output_logs.s1aplnk,
                zmvo=subscriber.output_logs.zmvo,
            ),
            network=NetworkModel(
                technology=subscriber.network.technology,
                enodeb=EnodeBModel(
                    name=subscriber.network.enodeb.name,
                    enodeb_id=subscriber.network.enodeb.enodeb_id,
                    link_status=subscriber.network.enodeb.link_status,
                    ip_address1=subscriber.network.enodeb.ip_address1,
                    ip_address2=subscriber.network.enodeb.ip_address2,
                    port=subscriber.network.enodeb.port,
                ),
                cell=CellModel(
                    bts_id=subscriber.network.cell.bts_id,
                    bts_name=subscriber.network.cell.bts_name,
                    bts_state=subscriber.network.cell.bts_state,
                    bsc_name=subscriber.network.cell.bsc_name,
                    bsc_id=subscriber.network.cell.bsc_id,
                ),
                nodeb=NodeBModel(
                    sa_name=subscriber.network.nodeb.sa_name,
                    sa_id=subscriber.network.nodeb.sa_id,
                    lac_id=subscriber.network.nodeb.lac_id,
                    administrative_state=subscriber.network.nodeb.administrative_state,
                ),
            ),
        )
        model_list.append(subscriber)
    return model_list

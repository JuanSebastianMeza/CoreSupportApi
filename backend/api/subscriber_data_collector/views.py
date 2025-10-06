import asyncio
import logging

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound

from .models import Subscriber
from .serializers import SubscriberSerializer

from .team_notifier.teams_notifier import send_teams_file, send_teams_notification

from .check_subscriber import CheckSubscriberData
from .remote_data_source.nokia.remote_ssh_connection import RemoteSshConnectionImpl
from .remote_data_source.remote_data_repo import RemoteDataRepo
from .remote_data_source.huawei.remote_oss_connection import RemoteOssConnection
from .remote_data_source.huawei.remote_telnet_connection import TelnetShellImpl

logging.getLogger().setLevel(level=logging.INFO)
# to run uvicorn api.asgi:application --reload

# Create your views here.
@api_view(['GET'])
async def get_subscribers_data(request):
    msisdns = request.GET.get('msisdn')
    if msisdns:
        msisdn_list = [x.strip() for x in msisdns.split(',')]
        return Response({"msisdn": msisdn_list})
    logging.info(f"MSISDNs: {msisdn_list}")
    # Check if the MSISDNs are in the correct format
    for msisdn in msisdn_list:
        if not check_msisdn_format(msisdn):
            raise NotFound(f"Invalid MSISDN format: {msisdn}")
    try:
        subscribers = [Subscriber(msisdn=msisdn) for msisdn in msisdn_list]
        tasks_list = [
            asyncio.create_task(run_csd(subscriber)) for subscriber in subscribers
        ]
        subscribers_data_list = []
        for task in tasks_list:
            subscribers_data_list.append(await asyncio.shield(task))
        logging.info(f"subscriber_data_list: {subscribers_data_list}")

        serializer = SubscriberSerializer(subscribers_data_list, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.error(f"Error: {e}")
        raise NotFound(f"Error processing MSISDNs: {e}")
    

async def run_csd(subscriber):
    # Dependencies initialization

    telnet_connection = TelnetShellImpl()
    oss_connection = RemoteOssConnection(telnet_connection)
    ssh_connection = RemoteSshConnectionImpl()
    remote_repo = RemoteDataRepo(oss_connection, ssh_connection)

    csd = CheckSubscriberData(remote_repo)
    subscriber = await csd.check_subscriber(subscriber)
    notification = build_notification_message(subscriber)
    try:
        logging.info("Sending team notification")
        send_teams_notification(notification)
        logging.info("Sending team log file notification")

        with open("log_file.log", "w") as f:
            f.write(f"""
        mmctx:
        {subscriber.output_logs.mmctx}
        s1aplnk:
        {subscriber.output_logs.s1aplnk}
        zmvo:
        {subscriber.output_logs.zmvo}
        zepo:
        {subscriber.output_logs.zepo}
                    """
                    )

        send_teams_file("log_file.log")
    except Exception as e:
        logging.error(f"Error trying to send teams notification: {e}")
        return subscriber

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
<li><b>EnodeB ID:</b> {subscriber.network.enodeb.id}</li>
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

def check_msisdn_format(msisdn: str) -> bool:
    """Check if the MSISDN is in the correct format.
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
    if len(msisdn) > 15:
        return False
    if not msisdn.isdigit():
        return False
    if len(msisdn) < 5:
        return False
    return True
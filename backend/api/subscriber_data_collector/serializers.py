from adrf.serializers import ModelSerializer
from .models import CellModel, EnodeBModel, NodeBModel, NetworkModel, OutputLogsModel, SubscriberModel

class CellSerializer(ModelSerializer):
    class Meta:
        model = CellModel
        fields = [
            'bts_id',
            'bts_name',
            'bsc_id',
            'bsc_name',
            'bts_state',
        ]

class EnodeBSerializer(ModelSerializer):
    class Meta:
        model = EnodeBModel
        fields = [
            'name',
            'enodeb_id',
            'link_status',
            'ip_address1',
            'ip_address2',
            'port',
        ]

class NodeBSerializer(ModelSerializer):
    class Meta:
        model = NodeBModel
        fields = [
            'sa_name',
            'sa_id',
            'lac_id',
            'administrative_state',
        ]

class NetworkSerializer(ModelSerializer):
    cell = CellSerializer()
    enodeb = EnodeBSerializer()
    nodeb = NodeBSerializer()
    class Meta:
        model = NetworkModel
        fields = [
            'technology',
            'enodeb',
            'nodeb',
            'cell',
        ]

class OutputLogsSerializer(ModelSerializer):
    class Meta:
        model = OutputLogsModel
        fields = [
            'mmctx',
            'zepo',
            's1aplnk',
            'zmvo',
        ]

class SubscriberSerializer(ModelSerializer):
    output_logs = OutputLogsSerializer()
    network = NetworkSerializer()
    class Meta:
        model = SubscriberModel
        fields = [
            'imsi',
            'msisdn',
            'sgsn',
            'mss',
            'last_activity_cico',
            'last_activity_paco',
            'services',
            'routing_category',
            'network',
            'output_logs',
        ]
        
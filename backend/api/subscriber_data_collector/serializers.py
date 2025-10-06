from rest_framework import serializers
from .models import Cell, EnodeB, NodeB, Network, OutputLogs, Subscriber

class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = '__all__'

class EnodeBSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnodeB
        fields = '__all__'

class NodeBSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeB
        fields = '__all__'

class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = '__all__'

class OutputLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputLogs
        fields = '__all__'

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'
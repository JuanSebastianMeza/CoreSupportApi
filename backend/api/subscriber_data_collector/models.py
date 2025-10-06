from django.db import models

    
class Cell(models.Model):
    """
    Model representing a NodeB in a mobile network.
    """
    bts_name = models.CharField(max_length=255, blank=True, default="")
    bts_id = models.IntegerField(default=0)
    bsc_name = models.CharField(max_length=255, blank=True, default="")
    bsc_id = models.IntegerField(default=0)
    bts_state = models.CharField(max_length=50, blank=True, default="")

    def __str__(self):
        return f"{self.bts_name} ({self.bts_id})"

class EnodeB(models.Model):
    """
    Model representing an eNodeB (Evolved Node B) in a mobile network.
    """
    name = models.CharField(max_length=255, blank=True, default="", help_text="Cell ID")
    enodeb_id = models.IntegerField(default=0, help_text="Enodeb ID in decimal format")
    link_status = models.CharField(max_length=100, blank=True, default="", help_text="Link status, normal status is connected")
    ip_address1 = models.GenericIPAddressField(blank=True, null=True, help_text="eNodeB IP address 1")
    ip_address2 = models.GenericIPAddressField(blank=True, null=True, help_text="eNodeB IP address 2")
    port = models.IntegerField(default=0, help_text="eNodeB port")

    def __str__(self):
        return f"{self.name} ({self.enodeb_id})"
    
class NodeB(models.Model):
    """
    Model representing a NodeB in a mobile network.
    """
    sa_name = models.CharField(max_length=255, blank=True, default="", help_text="Name of the NodeB")
    sa_id = models.IntegerField(default=0, help_text="NodeB ID in decimal format")
    lac_id = models.IntegerField(default=0, help_text="LAC in decimal format")
    administrative_state = models.CharField(max_length=50, blank=True, default="", help_text="State could be lock or unlocked")

    def __str__(self):
        return f"{self.sa_name} ({self.sa_id})"
   
class Network(models.Model):
    TECHNOLOGY_CHOICES = [
        ("LTE", "LTE"),
        ("UMTS", "UMTS"),
        ("GSM", "GSM"),
        ("", "Unknown"),
    ]
    technology = models.CharField(
        max_length=10,
        choices=TECHNOLOGY_CHOICES,
        default="",
        help_text="User current network technology (LTE, UMTS, GSM)",
    )
    enodeb = models.ForeignKey(
        EnodeB,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="If user is in 4g it shows the nodeb id",
    )
    nodeb = models.ForeignKey(
        'NodeB',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="If user is in 3g it shows the nodeb data",
    )
    cell = models.ForeignKey(
        Cell,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="If user is in 2g it shows the cell data",
    )

    def __str__(self):
        return f"{self.technology} Network"

class OutputLogs(models.Model):
    """
    Model representing output logs for various commands in a mobile network.
    """
    mmctx = models.TextField(blank=True, default="", help_text="Output log of mmctx command")
    zepo = models.TextField(blank=True, default="", help_text="Output log of zepo command")
    s1aplnk = models.TextField(blank=True, default="", help_text="Output log of s1aplnk command")
    zmvo = models.TextField(blank=True, default="", help_text="Output log of zmvo command")

    def __str__(self):
        return f"OutputLogs(mmctx={bool(self.mmctx)}, zepo={bool(self.zepo)}, s1aplnk={bool(self.s1aplnk)}, zmvo={bool(self.zmvo)})"

class Subscriber(models.Model):
    """
    Model representing a mobile network subscriber.
    """
    imsi = models.CharField(
        max_length=32,
        blank=True,
        default="",
        help_text="International Mobile Subscriber Identity"
    )
    msisdn = models.CharField(
        max_length=32,
        blank=True,
        default="",
        help_text="Mobile Station International Subscriber Directory Number"
    )
    sgsn = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Current user's SGSN"
    )
    mss = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Current user's MSS"
    )
    last_activity_cico = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Current user's last activity (CICO)"
    )
    routing_category = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Current user's routing category"
    )
    services = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Current user's services"
    )
    last_activity_paco = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="User last time activity saw from PACO side"
    )
    network = models.ForeignKey(
        Network,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Data of user current network technologies (LTE, UMTS, GSM)"
    )
    output_logs = models.ForeignKey(
        OutputLogs,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Output logs of the commands"
    )

    def __str__(self):
        return f"Subscriber(IMSI={self.imsi}, MSISDN={self.msisdn})"

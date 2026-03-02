// ─── Subscriber Data Interfaces ───────────────────────────────────────────────
// Mirrors the Django serializer models returned by GetSubscribersData (APIView)

export interface OutputLogs {
    mmctx: string;
    s1aplnk: string;
    zepo: string;
    zmvo: string;
}

export interface EnodeB {
    name: string;
    enodeb_id: number;
    link_status: string;
    ip_address1: string;
    ip_address2: string;
    port: number;
}

export interface NodeB {
    sa_name: string;
    sa_id: number;
    lac_id: number;
    administrative_state: string;
}

export interface Cell {
    bts_id: number;
    bts_name: string;
    bts_state: string;
    bsc_name: string;
    bsc_id: number;
}

export interface Network {
    technology: string;
    enodeb: EnodeB;
    nodeb: NodeB;
    cell: Cell;
}

export interface Subscriber {
    msisdn: string;
    imsi: string;
    vlr: string;
    sgsn: string;
    mss: string;
    last_activity_cico: string;
    last_activity_paco: string;
    routing_category: string;
    services: string;
    output_logs: OutputLogs;
    network: Network;
}

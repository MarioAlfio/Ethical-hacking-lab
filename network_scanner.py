#!/usr/bin/env python
"""
Network Scanner - Scoperta di dispositivi sulla rete locale tramite ARP
Utilizza la funzione arping di Scapy per inviare richieste ARP broadcast
"""

import scapy.all as scapy


def scan(ip):
    """
    Esegue uno scan ARP sulla rete specificata.
    
    Funzionamento:
    - Invia pacchetti ARP "Who has X?" in broadcast
    - I dispositivi attivi rispondono con il proprio MAC address
    - arping() stampa automaticamente i risultati
    
    Args:
        ip: Indirizzo IP o range CIDR (es. "192.168.1.0/24")
    """
    scapy.arping(ip)


# === ESECUZIONE ===
# Scansiona tutti i dispositivi nella sottorete /24
# Il /24 indica che verranno scansionati gli IP da .1 a .254
scan("192.168.1.1/24")

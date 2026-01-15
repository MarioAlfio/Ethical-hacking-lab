# Ethical-hacking-lab

Repository di strumenti e script per lo studio della cybersecurity e del penetration testing.

## Lab Setup

Tutti gli script sono testati in un ambiente virtualizzato isolato:

| Macchina | Sistema Operativo | Ruolo |
|----------|-------------------|-------|
| Attacker | Kali Linux | Esecuzione degli attacchi |
| Target | Windows | Bersaglio degli attacchi |

Le VM comunicano su una rete NAT/Host-only isolata dalla rete di produzione.

## Progetti

| Progetto | Descrizione |
|----------|-------------|
| [network-scanner](./network_scanner.py) | Scoperta di dispositivi attivi sulla rete tramite ARP |
| [arp-spoofer](./arp_spoof.py) | Attacco Man-in-the-Middle tramite ARP spoofing |

## Requisiti

- Python 3.x
- Scapy (`pip install scapy`)
- Privilegi root/admin per l'invio di pacchetti raw

## ⚠️ Disclaimer

Questi strumenti sono creati **esclusivamente per scopi educativi** e devono essere utilizzati solo in ambienti di laboratorio autorizzati o su sistemi di cui si possiede esplicita autorizzazione.

L'uso non autorizzato di questi strumenti su reti o sistemi altrui è **illegale** e può comportare conseguenze penali. L'autore non si assume alcuna responsabilità per usi impropri.

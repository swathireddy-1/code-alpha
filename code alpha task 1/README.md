# Basic Network Sniffer (Python)

A small command-line packet monitor built with **Python** and **Scapy**. It
shows network metadata such as source/destination IP addresses, protocol,
ports (when applicable), timestamps, and packet length.

## Privacy and authorized-use note

Use this program only on your own device, your own lab network, or a network
for which you have clear permission to monitor. Monitoring other people's
traffic without permission can violate privacy and applicable law.

**This project is intentionally metadata-only:**
- It does not display, decode, save, or export packet payloads.
- It does not collect passwords, messages, cookies, or other application data.
- It does not save packet captures to disk.
- `store=False` prevents Scapy from retaining captured packets in memory.

## Project files

```text
basic_network_sniffer/
├── sniffer.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.9 or newer
- Scapy
- Packet-capture support for your operating system:
  - **Windows:** install [Npcap](https://npcap.com/) and enable its loopback
    support if you need to monitor loopback traffic.
  - **Linux:** packet capture may require `sudo` or suitable capture
    capabilities.
  - **macOS:** packet capture may require administrator privileges.

## Installation

Create and activate a virtual environment (recommended), then run:

```bash
python -m pip install -r requirements.txt
```

## Find your network interface

Scapy can list available interfaces:

```bash
python -c "from scapy.all import get_if_list; print('\n'.join(get_if_list()))"
```

Choose an interface belonging to your own device or authorized lab.

## Run

On Linux/macOS, elevated privileges may be needed:

```bash
sudo python sniffer.py --interface eth0
```

On Windows, open a terminal as Administrator and use the interface name
reported by Scapy:

```powershell
python sniffer.py --interface "Wi-Fi"
```

Capture only a limited number of packets:

```bash
python sniffer.py --interface eth0 --count 25
```

Use a narrower header-level capture filter:

```bash
python sniffer.py --interface eth0 --filter "tcp or udp"
```

Stop a running capture with **Ctrl+C**.

## Example output

```text
2026-11-26 13:40:00 IST | IPv4/TCP | 192.168.1.10 -> 93.184.216.34 | ports=51522 -> 443 | length=74 bytes
2026-11-26 13:40:01 IST | IPv4/UDP | 192.168.1.10 -> 192.168.1.1 | ports=53000 -> 53 | length=72 bytes
```

The addresses and values above are illustrative examples, not live network data.

## Common issues

- **Scapy missing:** run `python -m pip install -r requirements.txt`.
- **Permission denied:** run the terminal with the required capture permissions.
- **No packets appear:** confirm the interface name, generate ordinary traffic
  on your own device, and check that the capture filter matches that traffic.
- **Windows capture errors:** verify that Npcap is installed correctly.

## How it works

1. Scapy listens on the selected network interface.
2. A BPF filter limits which packets are delivered to the program.
3. The program checks packet headers for IPv4, IPv6, ARP, TCP, UDP, and ICMP.
4. It prints a concise metadata summary and discards the packet.

## Learning goals

- Recognize common network protocols.
- Understand source and destination IP addresses.
- Identify TCP/UDP port numbers.
- Practice using Python command-line arguments and packet-capture libraries.

## License

You may use and modify this learning project for personal study and
authorized testing. Check Scapy's license and your local rules before
redistributing or deploying it.

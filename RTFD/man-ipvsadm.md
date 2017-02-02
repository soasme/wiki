# IPVSADM

- Purpose: set up, maintain and inspect the virtual server table in the Linux kernel.
- LVS
    - build scalable network services based on a cluster of two or more nodes.
- Features:
    - command
        - add service
            - support tcp / udp
            - persistent: for consistent connections
            - grouping virtual service by firewall mark (int)
            - grouping clients to hosts by netmask (such as 255.255.255.255)
            - packet forwarding methods
                - gatewaying, aka. direct routing
                - masquerading, aka. NAT (network  access  translation)
                - ipip encapsulation, aka. tunneling
            - scheduler
                - rr: round robin
                - wrr: weighted round robin
                - lc: least connection
                - wlc
                - lblc: locality-based lc
                - lblcr: lblc with replication
                - dh: destination hashing
                - sh: source hashing
                - sed: shortest expected delay
                - nq: never queue, fallback to sed if queueing
        - edit service
        - delete service
        - add server
        - edit server
        - delete server
        - list LVS table
        - clear LVS table
        - restore LVS table to rules line by line from stdin
        - save LVS table by dumping to stdout
        - zero counters for services
        - set timeout in seconds for tcp, after_tcp_fin_packet, udp
        - start daemon as master or backup
        - stop daemon
- defense DDoS
    - why vulnerable: each connection occupies 127 bytes memory, Dos -> OOM
    - strategy:
        - randomly drop some entries in the table
        - use secure tcp state transition table
        - use short timeouts

## Examples

### Simple Virtual Service

    ipvsadm -A -t 207.175.44.110:80 -s rr
    ipvsadm -a -t 207.175.44.110:80 -r 192.168.10.1:80 -m
    ipvsadm -a -t 207.175.44.110:80 -r 192.168.10.2:80 -m
    ipvsadm -a -t 207.175.44.110:80 -r 192.168.10.3:80 -m
    ipvsadm -a -t 207.175.44.110:80 -r 192.168.10.4:80 -m
    ipvsadm -a -t 207.175.44.110:80 -r 192.168.10.5:80 -m

### Firewall-mark Virtual Service

    ipvsadm -A -f 1  -s rr
    ipvsadm -a -f 1 -r 192.168.10.1:0 -m
    ipvsadm -a -f 1 -r 192.168.10.2:0 -m
    ipvsadm -a -f 1 -r 192.168.10.3:0 -m
    ipvsadm -a -f 1 -r 192.168.10.4:0 -m
    ipvsadm -a -f 1 -r 192.168.10.5:0 -m

---

- [Source](http://linuxcommand.org/man_pages/ipvsadm8.html)

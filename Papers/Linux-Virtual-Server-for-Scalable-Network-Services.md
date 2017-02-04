# Linux Virtual Server for Scalable Network Services

## Background

Increasing workload, Rapid Response, 24x7 Availability.
We can deploy clusters of servers, connected by a fast network.
By doing this, we need address some issues.

## Introduction

> Linux Virtual Server directs network connections to the
> different servers according to scheduling algorithms and
> makes parallel services of the cluster to appear as a virtual
> service on a single IP address. Client applications
> interact with the cluster as if it were a single server. The
> clients are not affected by interaction with the cluster
> and do not need modification. Scalability is achieved by
> transparently adding or removing a node in the cluster.
> High availability is provided by detecting node or daemon
> failures and reconfiguring the system appropriately.

The three-tier architecture of LVS:

- Load balancer
    - all the work is performed inside the kernel. Therefor, the overhead is low.
    - handle large number of connections than a general server.
    - backup lb to fix SPOF: Two heartbeat daemons run on primary and backup.
        - Failover and Takeover cause current connections lost, forcing client to resend request.
- Server pool
    - idential servers
    - replicated for either scalability and high availability.
    - failure detection to remove unavailable nodes from cluster.
- Backend storage
    - usually be distributed fault-tolerant file systems.

## IP Load Balancing Techniques

Aka. LVS/NAT, LVS/TUN, LVS/DSR.

### NAT (Network Address Translation)

- Foundation
    - Headers of packets can be adjusted. Servers believe they are contacted directly to clients, whilst clients believe they are contacting one IP address.
- Architecture
    - LB and real servers are interconnected by a switch or hub.
- Workflow
    - A user access virtual service  provided by the server cluster.
    - A request packet destined for VIP address arrived at the load balancer.
    - The load balancer examines the packet's destination address and port number.
    - The load balancer selected one of the servers from cluster by a scheduling algorithm.
    - The request packet's destination address and port are rewritten to the selected server.
    - The packet is forwarded to the server.
    - The load balancer keep rewriting incoming packets belongs to a connection in hash table.
    - The load balancer rewrite response packets to source address and port.
    - The load balancer remove connection record after connection terminated or timeout.

### TUN (tunneling)

- Foundation
    - Encapsulate IP datagram within IP datagram. The datagram destined for one IP address is wrapped and redirected to another IP address.
- Architecture
    - The real server: any server in any network supported IP tunneling protocol.
    - All real servers have one of their tunnel devices configured with VIP.
- Workflow
    - The same as NAT.
    - The load balancer encapsulates the packet within an IP datagram and forwards it to selected server.
    - The server decapsulates the packet and finds the inside packet.
    - The server processes the request and returns the result to user directly.

### DR (Direct Routing)

- Foundation
    - MAC address, ** NOT IP ADDRESS**, is used for Ethernet.
- Architecture
    - The load balancer and real servers are within the same physical network segment.
    - The VIP address is shared by the load balancer and real servers.
    - All real servers have their loopback alias interface configured with the VIP address.
    - The load balancer has an interface configured with the VIP address to accept incoming packets.
- Workflow
    - The same as NAT or TUN.
    - The load balancer directly routes a packet to the selected server by changing MAC address of data frame and retransmits it on the LAN.
    - The server receives the forwarded packet.
    - The server finds that the packet is for the address on its loopback alias interface, so it processes the request and return the result directly to the user.
    - Real servers' interfaces that are configured with VIP address should not do ARP response, otherwise there will be collision.

## Comparison of LVS/NAT, LVS/TUN, LVS/DR

    |                | LVS/NAT       | LVS/TUN    | LVS/DR      |   |
    |----------------|---------------|------------|-------------|---|
    | Server         | any           | tunneling  | non-arp dev |   |
    | Server Network | private       | LAN/WAN    | LAN         |   |
    | Server Number  | low (10˜20)   | high (100) | high (100)  |   |
    | Server Gateway | load balancer | own router | own router  |   |

- LVS/NAT
    - Pros
        - Real servers can run any OS supportted TCP
        - Only one address is needed for load balancer
    - Cons
        - Bad scalability: rewrite packets need consume CPU resource. It exists upper bound.
- LVS/TUN
    - Pros
        - Good scalability
    - Cons
        - Servers need support IP Tunneling protocol. (Of course, IP Tunneling protocol is becoming a stardard of all OS)
- LVS/DR
    - Pros
        - Good scalability
    - Cons
        - Server has loopback alias interface that doesn't do ARP resonse.
        - The load balancer and real servers must be connected

## Implemention Issues

![](http://g.gravizo.com/g?%20digraph%20G%20{%20%22VS%20Schedule%20&%20Control%20Module%22%20-%3E%20%22VS%20Rules%20Table%22;%20%22VS%20Schedule%20&%20Control%20Module%22%20-%3E%20%22Connection%20Hash%20Table%22;%20%22VS%20Schedule%20&%20Control%20Module%22%20-%3E%20IPVSADM;%20IPVSADM%20-%3E%20%22VS%20Schedule%20&%20Control%20Module%22;%20})

- Main Module hooks inside kernel to grab IP packets.
- Main Module hooks inside kernel to rewrite IP packets.
- Main Module looks up the "VS Rules" hash table for new connections.
- Main Module checks the "Connection Hash Table" for established connections.
- IPVSADM is user-space program to administratior virtual servers by setsockopt and `/proc`.
- Connection Hash Table hold millions of concurrent connections.
- Each Connection occupies 128 bytes of memory.
- Slow timer is ticked every second to collect stale connections.
- LVS implements ICMP handling.

## Connection Scheduling

- Round-Robin
- Weighted Round-Robin
- Least-Connection
    - dynamic: count active connections

Connection Affinity:

- FTP is connection affinity. FTP requires server hold 2 ports - 20 for control connection, 21 for bulk data transfer. But LVS/NAT, LVS/DR only only on the client-to-server half connection, so it's impossible for LVS to get the port from the packets that goes to client directly.
- SSL is connection affinity for performance reason: Since it is time-consuming to negociate and generate the SSL key, the successive connections from the same client can also be granted by the server in the life span of the SSL key.
- How to solve it? - Add persistent port handling.
    - mark service as persistent.
    - Load balancer create connection template
    - Load balancer create an entry for connection in the table
    - Before the template expires, the connection for any port from client will send to the ring server according to the template.

## Cluster Management

- setup and manage clusters.
- self-configuration with respect to different load contribution and self-heal with node/service failure and recovery.
- solutions
    - Piranha
        - `nanny` daemon is to monitor server nodes and the corresponding services in the cluster
            - receive the response from the server node and the service in a specific time
            - otherwise remove the server from scheduling table in the kernel
            - dynamically adjust the weight to avoid the server overloaded
        - `pulse` daemon is to control the `nanny` daemons and handle failover between 2 lbs.
    - lvs-gui + heartbeat + ldirectord
    - mon + heartbeat

## Limitation

- LVS only support IP load balancing techniques, so it cannot do content-based scheduling for different servers.
- The failover and takeover of primary load balancer to backup will cause the established connections in the state table lost. - Just resend it.

Source: [Linux Virtual Server for Scalable Network Services](http://www.linuxvirtualserver.org/ols/lvs.pdf)

# NF10WV-NAT-Fixer

The Netcomm NF10WV, by default, only performs NAT for the directly connected local
network. You can, however, telnet into the router and manually fiddle with iptables
to make it do NAT and provide internet access to all networks reachable through
the router's LAN interface.

Unfortunately, any changes made with iptables are lost when the router reboots or
simply loses its connection to the internet.

This python script connects to the modem, checks to see if the required MASQUERADE
line is still there, and adds it if it isn't.

I run this script every 5 minutes with cron.

// Inside your NS-3 Application
Ptr<Socket> ns3Socket = Socket::CreateSocket (GetNode (), UdpSocketFactory::GetTypeId ());
InetSocketAddress remote = InetSocketAddress (Ipv4Address ("127.0.0.1"), 5005);
ns3Socket->Connect (remote);

// When a packet is generated:
std::string trafficType = "DDoS"; // or "Normal"
Ptr<Packet> p = Create<Packet> (reinterpret_cast<const uint8_t*> (trafficType.c_str()), trafficType.length());
ns3Socket->Send (p);
import http.server
import socketserver
import arpreq
import fileinput
import os
import yaml


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
  def do_GET(self):

    with open('server-config.yaml') as f:

      clients = yaml.load(f, Loader=yaml.FullLoader)
    
    
    client_address = super(http.server.SimpleHTTPRequestHandler, self).address_string()
    client_mac = arpreq.arpreq(client_address)
    print(client_address)
    print(client_mac)

    
    f1 = open('config.fcc', 'r')
    f2 = open('config2.fcc', 'w')
    
    if client_mac in clients:
      checkWords = ("hostname_node","ipaddress_eth0","gateway_eth0",
              "macaddress_eth0","macaddress_eth1",
              "macaddress_eth2","ipaddress_team0","gateway_team0")
      
      repWords = (clients[client_mac][0]["eth0"]["hostname"],
              clients[client_mac][0]["eth0"]["ip_address"],
              clients[client_mac][0]["eth0"]["gateway"],
              clients[client_mac][0]["eth0"]["mac_address"],
              clients[client_mac][1]["eth1"]["mac_address"],
              clients[client_mac][2]["eth2"]["mac_address"],
              clients[client_mac][3]["team0"]["ip_address"],
              clients[client_mac][3]["team0"]["gateway"])

      for line in f1:
        for check, rep in zip(checkWords, repWords):
          line = line.replace(check, rep)
        f2.write(line)
      f1.close()
      f2.close()

      os.system('/usr/src/app/fcct --pretty --strict /usr/src/app/config.fcc > ignition.ign')
    
      if self.path == '/config.ign':
        self.path = 'ignition.ign'
      return http.server.SimpleHTTPRequestHandler.do_GET(self)

    else:
      return false


# Create an object of the above class
handler_object = MyHttpRequestHandler

PORT = 8000
my_server = socketserver.TCPServer(("", PORT), handler_object)
print("Server started at localhost:" + str(PORT))
# Star the server
my_server.serve_forever()

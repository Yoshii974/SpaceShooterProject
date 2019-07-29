from socket import *
from NetworkEngine import *

ne_server = NetworkEngine()
ne_server.initialization()

ss = socket.socket(AF_INET, SOCK_DGRAM)
ss.bind(("localhost", 63200))

ne_server.setDependencies(63201, "localhost", ss)

data1_server = ["data from server", [-9.8234, "lala"], {'a':54, 'b':-32}]
data2_server = "juste une string en provenance du serveur"




ne_client = NetworkEngine()
ne_client.initialization()

sc = socket.socket(AF_INET, SOCK_DGRAM)
sc.bind(("localhost", 63201))

ne_client.setDependencies(63200, "localhost", sc)

data1_client = ["data from client", {'a':54, 'b':-32}, [[], "lala"]]
data2_client = "juste une string en provenance du client"


ne_server.encodeData(data1_server)
ne_server.encodeData(data2_server)
ne_client.decodeData()
print(ne_client.lastDataReceived)
ne_client.decodeData()
print(ne_client.lastDataReceived)
import Pyro4

server_uri = "PYRONAME:TESTE"
server = Pyro4.Proxy(server_uri)
server.register_client("client_reference")




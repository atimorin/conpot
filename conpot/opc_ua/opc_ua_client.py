import socket

from construct import Struct, String, ULInt32, PascalString, Container


c = Struct(
    'OPC UA TCP Hello Message',
    String('MessageType', 3),
    String('Reserved', 1),
    ULInt32('MessageSize'),
    ULInt32('ProtocolVersion'),
    ULInt32('ReceiveBufferSize'),
    ULInt32('SendBufferSize'),
    ULInt32('MaxMessageSize'),
    ULInt32('MaxChunkCount'),
    PascalString('EndpointUrl', length_field=ULInt32('length'), encoding='utf8'),
)

x = Container(
    MessageType='HEL',
    Reserved='F',
    MessageSize=53,
    ProtocolVersion=0,
    ReceiveBufferSize=9000,
    SendBufferSize=9000,
    MaxMessageSize=0,
    MaxChunkCount=0,
    EndpointUrl='opc.tcp://opycua:4841',
)

packed_data = c.build(x)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 4840)
sock.connect(server_address)
try:
    # Send data
    print 'sending {0}'.format(packed_data)
    sock.sendall(packed_data)
finally:
    print 'closing socket'
    sock.close()

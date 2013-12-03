# Copyright (C) 2013  Lukas Rist <glaslos@gmail.com>
# Copyright (C) 2012  Jan Costermans
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import logging

from gevent.server import StreamServer
from construct import String, ULInt32, PascalString, Struct

logger = logging.getLogger(__name__)


class OpcUaServer(object):
    """
    Based on OPyCua snippets by Jan Costermans
    """
    def __init__(self):
        self.c = Struct(
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

    def handle(self, socket, address):
        logger.debug("New connection: {0}".format(address))
        try:
            data = socket.recv(53)
            logger.debug('Received: {0}'.format(data))
            unpacked_data = self.c.parse(data)
            logger.debug('Unpacked: {0}'.format(unpacked_data))
        finally:
            socket.close()

    def get_server(self, host, port):
        connection = (host, port)
        server = StreamServer(connection, self.handle)
        logger.info('OPC UA server started on: {0}'.format(connection))
        return server


if __name__ == "__main__":
    ous = OpcUaServer()
    server = ous.get_server("localhost", 4840)
    server.serve_forever()

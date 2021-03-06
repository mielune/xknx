"""Abstraction to send ConnectRequest and wait for ConnectResponse."""
from xknx.knxip import (
    HPAI,
    ConnectRequest,
    ConnectRequestType,
    ConnectResponse,
    KNXIPFrame,
)

from .request_response import RequestResponse


class Connect(RequestResponse):
    """Class to send a ConnectRequest and wait for ConnectResponse.."""

    def __init__(self, xknx, udp_client, net_bind=None):
        """Initialize Connect class."""
        self.udp_client = udp_client
        super().__init__(xknx, self.udp_client, ConnectResponse, net_bind=net_bind)
        self.communication_channel = 0
        self.identifier = 0

    def create_knxipframe(self) -> KNXIPFrame:
        """Create KNX/IP Frame object to be sent to device."""
        (local_addr, local_port) = self.udp_client.getsockname()
        # set control_endpoint and data_endpoint to the same udp_connection
        if self.net_bind and self.net_bind[0]:
            endpoint = HPAI(ip_addr=self.net_bind[0], port=self.net_bind[1])
        else:
            endpoint = HPAI(ip_addr=local_addr, port=local_port)
        connect_request = ConnectRequest(
            self.xknx,
            request_type=ConnectRequestType.TUNNEL_CONNECTION,
            control_endpoint=endpoint,
            data_endpoint=endpoint,
        )
        return KNXIPFrame.init_from_body(connect_request)

    def on_success_hook(self, knxipframe):
        """Set communication channel and identifier after having received a valid answer."""
        self.communication_channel = knxipframe.body.communication_channel
        self.identifier = knxipframe.body.identifier

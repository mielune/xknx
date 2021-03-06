"""Abstraction to send ConnectonStateRequest and wait for ConnectionStateResponse."""
from xknx.knxip import HPAI, ConnectionStateRequest, ConnectionStateResponse, KNXIPFrame

from .request_response import RequestResponse


class ConnectionState(RequestResponse):
    """Class to send ConnectonStateRequest and wait for ConnectionStateResponse."""

    def __init__(self, xknx, udp_client, communication_channel_id, net_bind=None):
        """Initialize ConnectionState class."""
        self.udp_client = udp_client
        super().__init__(xknx, self.udp_client, ConnectionStateResponse, net_bind=net_bind)
        self.communication_channel_id = communication_channel_id

    def create_knxipframe(self) -> KNXIPFrame:
        """Create KNX/IP Frame object to be sent to device."""
        (local_addr, local_port) = self.udpclient.getsockname()
        if self.net_bind:
            endpoint = HPAI(ip_addr=self.net_bind[0], port=self.net_bind[1])
        else:
            endpoint = HPAI(ip_addr=local_addr, port=local_port)
        connectionstate_request = ConnectionStateRequest(
            self.xknx,
            communication_channel_id=self.communication_channel_id,
            control_endpoint=endpoint,
        )
        return KNXIPFrame.init_from_body(connectionstate_request)

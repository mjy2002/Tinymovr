
import time

from tinymovr.iface import (create_frame, create_id,
    filter_id_from_node_id, filter_mask_from_node_id)

class CANNode:
    '''
    A class implementing a CAN Node over a python-can bus
    '''
    def __init__(self, node_id, bus):
        self.node_id = node_id
        bus.set_filters([{
            "can_id": filter_id_from_node_id(node_id),
            "can_mask": filter_mask_from_node_id(node_id),
            "extended": False
        }])
        self.bus = bus

    def send(self, msg, delay=0.001):
        self.bus.send(msg)
        time.sleep(delay)

    def send_new(self, endpoint_id, rtr=False, payload=None):
        self.bus.send(create_frame(self.node_id,
            endpoint_id, rtr, payload))

    def receive(self, endpoint_id):
        for frame in self.bus:
            return frame.data



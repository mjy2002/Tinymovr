
import can
import serial
from serial.tools import list_ports

ifaces_to_devices = {
    "slcan": ("canable", "cantact"),
    "robotell": ("CP210", )
}

CAN_EP_SIZE = 6

def guess_channel(iface_hint):
    '''
    Tries to guess a channel based on an interface hint.
    '''
    device_strings = [s.lower() for s in ifaces_to_devices[iface_hint]]
    ports = []
    for p in serial.tools.list_ports.comports():
        desc_lower = p.description.lower()
        if any([s in desc_lower for s in device_strings]):
            ports.append(p.device)
    if not ports:
        raise IOError("Could not autodiscover CAN channel")
    if len(ports) > 1:
        logging.warning('Multiple channels discovered - using the first')
    
    return ports[0]

def create_frame(node_id, endpoint_id, rtr=False, payload=None):
    '''
    Generate and return a CAN frame using python-can Message class
    '''
    return can.Message(arbitration_id=create_id(node_id, endpoint_id),
                        is_extended_id=False,
                        is_remote_frame=rtr,
                        data=payload)

def create_id(node_id, endpoint_id):
    '''
    Generate a CAN id from node and endpoint ids
    '''
    return filter_id_from_node_id() | endpoint_id

def filter_id_from_node_id(node_id):
    '''
    Generate a CAN filter id from given node ID
    '''
    return node_id << CAN_EP_SIZE

def filter_mask_from_node_id(node_id):
    '''
    Generate a CAN filter mask from given node ID
    '''
    return 0xFF << CAN_EP_SIZE
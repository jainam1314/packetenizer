from .helper import module
from scapy.plist import PacketList
class CoreStructure:
    '''
    This is the root of all class where the core
    dictionary is stored
    '''
    _core_dict = dict()
    _packets = None

    def __init__(self, scapy_packets: PacketList):
        '''
        It expects a scapy parsed dump file
        '''
        self._packets = scapy_packets

    def start(self):
        '''
        This function begins the actual analysis of scapy parsed file
        '''
        for packet in self._packets:
            s_socket, d_socket = (None, None)
            try:
                s_socket, d_socket = module.extract_socket(packet)
            except:
                print(f'Error:{packet}')
            if not s_socket or not d_socket:
                continue
                # print('Ughh.. Problem')
                # print(module.debug_packet(packet))
            else:
                if not (s_socket, d_socket) in self._core_dict:
                    if not (d_socket, s_socket) in self._core_dict:
                        # The connection doesn't exist create a new one
                        self._core_dict[(s_socket, d_socket)] = module.create_connection(packet)
                    else:
                        # The connection does exist just set the swap=true
                        self._core_dict[(d_socket, s_socket)].update(packet, swap=True)
                else:
                    self._core_dict[(s_socket, d_socket)].update(packet)

    def __str__(self):
        return self._core_dict.__str__()
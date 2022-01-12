from pydantic import BaseModel
from typing import List, Union, Dict
from enum import Enum
from typing import Optional
import yaml
import ipaddress


class Communities(BaseModel):
    """Model that represents all the communities"""

    std_communities: Dict[str, str]
    other_communities: Optional[Dict[str, str]] = None

    class Config:
        allow_mutation = False


class PLATFORM(str, Enum):
    juniper = "juniper"
    arista = "arista"


class MODEL(str, Enum):
    """Selection of possible models that can be used by the NetDevice class."""

    QFX10008 = "QFX10008"
    MX10008 = "MX10008"
    DCS_7050CX3_32S_R = "DCS-7050CX3-32S-R"
    DCS_7260CX3_64_R = "DCS-7260CX3-64-R"


class SubInterface(BaseModel):
    """Subinterface to an interface

    TODO: further implement this class"""

    name: str


class Layer3Interface(BaseModel):
    """Standard Layer 3 interface"""

    name: str
    device_name: str
    ipv4: Optional[ipaddress.IPv4Interface]
    ipv6: Optional[ipaddress.IPv6Interface]
    description: Optional[str]
    sub_interfaces: Optional[List[SubInterface]] = None


class Layer2Interface(BaseModel):
    """Standard Layer 2 interface

    TODO: further implement this class"""

    name: str


class NetDevice(BaseModel):
    """Network device schema"""

    name: str
    serial: str
    model: MODEL
    platform: PLATFORM
    mgmt: ipaddress.IPv4Interface
    role: str
    interfaces: List[Union[Layer3Interface, Layer2Interface]]
    communities: Optional[Communities] = None
    secrets: Optional[Dict[str, str]] = None

    class Config:
        use_enum_values = True


class Network(BaseModel):
    """Model that represents all the netdevices"""

    devices: List[NetDevice] = []

    class Config:
        use_enum_values = True


if __name__ == "__main__":
    # example on how to instantiate a both NetDevice as well as Network:
    network_device_1 = NetDevice(
        **yaml.safe_load(
            """
name: R1
serial: BX109
model: MX10008
platform: juniper
mgmt: 10.0.0.1/31
role: spine
interfaces:
  - name: et-0/0/0
    ipv4: 192.168.1.1/31
    description: core_link
  - name: et-0/0/1
    ipv4: 192.168.1.3/31
    description: core_link    
"""
        )
    )
    print(network_device_1.dict())

    network_device_2 = NetDevice(
        **yaml.safe_load(
            """
name: R2
serial: BX109
model: MX10008
platform: juniper
mgmt: 10.0.0.2/31
role: leaf
interfaces:
  - name: et-0/0/0
    ipv4: 192.168.1.5/31
    description: core_link
  - name: et-0/0/1
    ipv4: 192.168.1.7/31
    description: core_link    
"""
        )
    )
    print(network_device_2.dict())
    community_values = Communities(
        **yaml.safe_load(
            """
communities:
  COMMUNITY_1 : '1:1'
  COMMUNITY_2 : '2:2' 
  COMMUNITY_3 : '3:3'
"""
        )
    )
    print(community_values.dict())
    my_devices = [network_device_1, network_device_2]
    network = Network(
        **yaml.safe_load(
            """
devices:
- name: R1
  serial: BX109
  model: MX10008
  platform: juniper
  mgmt: 10.0.0.1/31
  role: spine
  interfaces:
    - name: et-0/0/0
      ipv4: 192.168.1.1/31
      description: core_link
    - name: et-0/0/1
      ipv4: 192.168.1.3/31
      description: core_link 
- name: R2
  serial: BX109
  model: MX10008
  platform: juniper
  mgmt: 10.0.0.2/31
  role: leaf
  interfaces:
    - name: et-0/0/0
      ipv4: 192.168.1.5/31
      description: core_link
    - name: et-0/0/1
      ipv4: 192.168.1.7/31
      description: core_link    
"""
        )
    )
    print(network.dict())

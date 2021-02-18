from dataclases import datalass
from drone import Drone
@dataclass
class Instruction:
    drone:Drone
    action:str
    
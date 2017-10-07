from ctypes import *
import psutil
from ctypes.wintypes import *

OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
CloseHandle = windll.kernel32.CloseHandle

class ProcessInjector:
    process_name = "MBAA.exe"
    PROCESS_ALL_ACCESS = 0x1F0FFF
    pid = 0
    processHandle = 0
    address = 0x010F93CC #Base address for 1p data, 10F9EC8 for 2p, record size 2812d
    address_2p = 0x010F9EC8
    dword_buffer = create_string_buffer(4)
    word_buffer = create_string_buffer(2)
    byte_buffer = create_string_buffer(1)

    def injectGameProcess(self):
        for proc in psutil.process_iter():
            process = psutil.Process(proc.pid)
            pname = process.name()
            if pname == self.process_name:
                print ("process found")
                self.pid = process.pid

        self.processHandle = OpenProcess(self.PROCESS_ALL_ACCESS, False, self.pid)
        if self.processHandle == 0:
            print("Failed to open process")

#StageData = namedtuple('StageData','1pHp 1pGauge 1pHeat 1pLocX 1pLocY 1pVelX 1pVelY 1pStatus 2pHp 2pGauge 2pHeat 2pLocX 2pLocY 2pVelX 2pVelY 2pStatus')
    def get1pHp(self):
        if ReadProcessMemory(self.processHandle, self.address, self.word_buffer, len(self.word_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.word_buffer,byteorder='little',signed=True)

    def get1pGauge(self):
        if ReadProcessMemory(self.processHandle, self.address+ 0x24, self.word_buffer, len(self.word_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.word_buffer,byteorder='little',signed=True)

    def get1pHeat(self):
        if ReadProcessMemory(self.processHandle, self.address+ 0x2c, self.word_buffer, len(self.word_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.word_buffer,byteorder='little',signed=True)

    def get1pLocX(self):
        if ReadProcessMemory(self.processHandle, self.address+ 0x4c, self.dword_buffer, len(self.dword_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.dword_buffer,byteorder='little',signed=True)

    def get1pLocY(self):
        if ReadProcessMemory(self.processHandle, self.address+ 0x50, self.dword_buffer, len(self.dword_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.dword_buffer,byteorder='little',signed=True)

    def get1pVelX(self):
        if ReadProcessMemory(self.processHandle, self.address+ 0x60, self.dword_buffer, len(self.dword_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.dword_buffer,byteorder='little',signed=True)

    def get1pVelY(self):
        if ReadProcessMemory(self.processHandle, self.address+ 0x64, self.dword_buffer, len(self.dword_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.dword_buffer,byteorder='little',signed=True)

    def get1pAttackState(self):
        if ReadProcessMemory(self.processHandle, self.address+ 0x260, self.byte_buffer, len(self.byte_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.byte_buffer,byteorder='little',signed=True)

    def get1pDamageState(self):
        if ReadProcessMemory(self.processHandle, self.address+ 0xF6, self.byte_buffer, len(self.byte_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.byte_buffer,byteorder='little',signed=True)

    def get2pHp(self):
        if ReadProcessMemory(self.processHandle, self.address_2p, self.word_buffer, len(self.word_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.word_buffer,byteorder='little',signed=True)

    def get2pGauge(self):
        if ReadProcessMemory(self.processHandle, self.address_2p+ 0x24, self.word_buffer, len(self.word_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.word_buffer,byteorder='little',signed=True)

    def get2pHeat(self):
        if ReadProcessMemory(self.processHandle, self.address_2p+ 0x2c, self.word_buffer, len(self.word_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.word_buffer,byteorder='little',signed=True)

    def get2pLocX(self):
        if ReadProcessMemory(self.processHandle, self.address_2p+ 0x4c, self.dword_buffer, len(self.dword_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.dword_buffer,byteorder='little',signed=True)

    def get2pLocY(self):
        if ReadProcessMemory(self.processHandle, self.address_2p+ 0x50, self.dword_buffer, len(self.dword_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.dword_buffer,byteorder='little',signed=True)

    def get2pVelX(self):
        if ReadProcessMemory(self.processHandle, self.address_2p+ 0x60, self.dword_buffer, len(self.dword_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.dword_buffer,byteorder='little',signed=True)

    def get2pVelY(self):
        if ReadProcessMemory(self.processHandle, self.address_2p+ 0x64, self.dword_buffer, len(self.dword_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.dword_buffer,byteorder='little',signed=True)

    def get2pAttackState(self):
        if ReadProcessMemory(self.processHandle, self.address_2p+ 0x260, self.byte_buffer, len(self.byte_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.byte_buffer,byteorder='little',signed=True)

    def get2pDamageState(self):
        if ReadProcessMemory(self.processHandle, self.address_2p+ 0xF6, self.byte_buffer, len(self.byte_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.byte_buffer,byteorder='little',signed=True)

    def getStageData(self):
        return [min_max_normalize(self.get1pHp(),5700,11400),
                min_max_normalize(self.get1pGauge(),15000,30000),
                min_max_normalize(self.get1pHeat(),1.5,3),
                min_max_normalize(self.get1pLocX(),0,131072),
                min_max_normalize(self.get1pLocY(),-32768,65536),
                min_max_normalize(self.get1pVelX(),800,1600),
                min_max_normalize(self.get1pVelY(),0,1600),
                min_max_normalize(self.get1pAttackState(),0,256),
                min_max_normalize(self.get1pDamageState(),0,256),
                min_max_normalize(self.get2pHp(),5700,11400),
                min_max_normalize(self.get2pGauge(),15000,30000),
                min_max_normalize(self.get2pHeat(),1.5,3),
                min_max_normalize(self.get2pLocX(),0,131072),
                min_max_normalize(self.get2pLocY(),-32768,65536),
                min_max_normalize(self.get2pVelX(),800,1600),
                min_max_normalize(self.get2pVelY(),0,1600),
                min_max_normalize(self.get2pAttackState(),0,256),
                min_max_normalize(self.get2pDamageState(),0,256),
                ]

    def stageDataPrettyPrint(self):
        print('1P HP:' + str(self.get1pHp()) + ';  1P Gauge:' + str(self.get1pGauge()) + ';  1P Heat:' + str(self.get1pHeat()) + ';  1P LocX:' + str(self.get1pLocX())
              + ';  1P LocY:' + str(self.get1pLocY()) + ';  1PVelX:' + str(self.get1pVelX()) + '; 1PVelY:' + str(self.get1pVelY()) +';  1PAttackState:' + str(self.get1pAttackState()) +'; 1PDamageState:' + str(self.get1pDamageState()))
        print('2P HP:' + str(self.get2pHp()) + ';  2p Gauge:' + str(self.get2pGauge()) + ';  2p Heat:' + str(self.get2pHeat()) + ';  2p LocX:' + str(self.get2pLocX())
              + ';  2p LocY:' + str(self.get2pLocY()) + ';  2pVelX:' + str(self.get2pVelX()) + '; 2pVelY:' + str(self.get2pVelY()) +';  2pAttackState:' + str(self.get2pAttackState()) +'; 2pDamageState:' + str(self.get2pDamageState()))

    def __init__(self):
        self.injectGameProcess()

    def __exit__(self, exc_type, exc_val, exc_tb):
        CloseHandle(self.processHandle)

def min_max_normalize(x,base,range):
    return 2*(x-base)/range

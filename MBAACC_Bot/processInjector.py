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
    dword_buffer = create_string_buffer(4)
    word_buffer = create_string_buffer(2)

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


    def get1pDamageState(self):
        if ReadProcessMemory(self.processHandle, self.address+ 0xF6, self.dword_buffer, len(self.dword_buffer), byref(c_ulong(0))):
            return int.from_bytes(self.dword_buffer,byteorder='little',signed=True)

    def stageDataPrettyPrint(self):
        print('1P HP:' + str(self.get1pHp()) + ';  1P Gauge:' + str(self.get1pGauge()) + ';  1P Heat:' + str(self.get1pHeat()) + ';  1P LocX:' + str(self.get1pLocX())
              + ';  1P LocY:' + str(self.get1pLocY()) + ';  1PVelX:' + str(self.get1pVelX()) + '; 1PVelY:' + str(self.get1pVelY()) +'; 1PDamageState:' + str(self.get1pDamageState()))


    def __init__(self):
        self.injectGameProcess()

    def __exit__(self, exc_type, exc_val, exc_tb):
        CloseHandle(self.processHandle)



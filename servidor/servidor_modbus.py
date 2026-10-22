from pyModbusTCP.server import DataBank, ModbusServer
import struct
import random
from time import sleep

class ServidorMODBUS():
    def __init__(self, host_ip, port):
        self._db = DataBank()
        self._server = ModbusServer(host=host_ip, port=port, no_block=True, data_bank=self._db)
        self.setpoint = 15.0
        self.vazao = 0.0
        
        self._db.set_holding_registers(700, self.float_to_regs(45.5 * 10))
        self._db.set_holding_registers(702, self.float_to_regs(46.1 * 10))
        self._db.set_holding_registers(704, self.float_to_regs(45.8 * 10))
        self._db.set_holding_registers(706, self.float_to_regs(38.0 * 10))
        self._db.set_holding_registers(710, self.float_to_regs(1.2))
        self._db.set_holding_registers(712, self.float_to_regs(self.vazao))
        self._db.set_holding_registers(830, [6000])
        self._db.set_holding_registers(840, [123])
        self._db.set_holding_registers(847, [3800])
        self._db.set_holding_registers(868, [950])
        self._db.set_holding_registers(1302, self.float_to_regs(self.setpoint))
        self._db.set_holding_registers(1328, [0])

    def float_to_regs(self, f_val):
        b = struct.pack('>f', float(f_val))
        return [struct.unpack('>H', b[0:2])[0], struct.unpack('>H', b[2:4])[0]]
    
    def regs_to_float(self, regs):
        b = struct.pack('>HH', regs[0], regs[1])
        return struct.unpack('>f', b)[0]

    def run(self):
        self._server.start()
        print("Servidor MODBUS em execução. Pressione Ctrl+C para sair.")
        try:
            while True:
                regs_sp = self._db.get_holding_registers(1302, 2)
                if regs_sp:
                    self.setpoint = self.regs_to_float(regs_sp)
                
                regs_cmd = self._db.get_holding_registers(1328, 1)
                if regs_cmd:
                    habilita = (regs_cmd[0] >> 6) & 1
                else:
                    habilita = 0

                if habilita:
                    erro = self.setpoint - self.vazao
                    self.vazao += erro * 0.1
                else:
                    self.vazao *= 0.9

                tensao = 380.0 + random.uniform(-2, 2)
                
                self._db.set_holding_registers(712, self.float_to_regs(self.vazao))
                self._db.set_holding_registers(847, [int(tensao * 10)])
                
                sleep(1)
        except KeyboardInterrupt:
            print("Servidor encerrado.")
            self._server.stop()

if __name__ == '__main__':
    s = ServidorMODBUS('localhost', 502)
    s.run()

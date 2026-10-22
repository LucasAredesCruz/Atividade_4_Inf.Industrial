from pymodbus.client import ModbusTcpClient
import struct

class ClienteMODBUS():
    def __init__(self, server_ip, porta):
        self._cliente = ModbusTcpClient(host=server_ip, port=porta)
    
    def conectar(self):
        return self._cliente.connect()
        
    def desconectar(self):
        self._cliente.close()

    def ler_holding_register(self, addr, count=1):
        resp = self._cliente.read_holding_registers(address=addr, count=count, slave=1)
        if resp and not resp.isError():
            return resp.registers
        return None

    def escrever_holding_register(self, addr, valor):
        resp = self._cliente.write_register(address=addr, value=valor, slave=1)
        if resp and not resp.isError():
            return True
        return False

    def ler_float32(self, addr):
        regs = self.ler_holding_register(addr, 2)
        if regs:
                b = struct.pack('>HH', regs[0], regs[1])
                return struct.unpack('>f', b)[0]
        return None

    def escrever_float32(self, addr, valor):

        b = struct.pack('>f', float(valor))
        regs = [struct.unpack('>H', b[0:2])[0], struct.unpack('>H', b[2:4])[0]]
            
        resp = self._cliente.write_registers(address=addr, values=regs, slave=1)
        if resp and not resp.isError():
            return True
        return False

    def ler_bits_registrador(self, addr):
        regs = self.ler_holding_register(addr, 1)
        if regs:
            valor = regs[0]
            bits = [(valor >> i) & 1 for i in range(16)]
            return bits
        return None

    def escrever_bit_individual(self, addr, bit_index, valor_bit):
        if not (0 <= bit_index <= 15) or valor_bit not in [0, 1]:
            return False
        
        regs = self.ler_holding_register(addr, 1)
        if not regs:
            return False
        
        valor_atual = regs[0]
        if valor_bit == 1:
            novo_valor = valor_atual | (1 << bit_index)
        else:
            novo_valor = valor_atual & ~(1 << bit_index)
            
        return self.escrever_holding_register(addr, novo_valor)

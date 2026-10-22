import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cliente.cliente_modbus import ClienteMODBUS
from time import sleep

if __name__ == "__main__":
    cliente = ClienteMODBUS('localhost', 502)
    if cliente.conectar():
        print("--- Demonstração Manipulação de Bits ---")
        
        endereco = 1328
        bits = cliente.ler_bits_registrador(endereco)
        print(f"Bits iniciais no registrador {endereco}:")
        for i, b in enumerate(bits):
            if b == 1: print(f"Bit {i}: {b}")
        
        print("\nAtivando bit 6 (Habilitar sistema)...")
        cliente.escrever_bit_individual(endereco, 6, 1)
        bits = cliente.ler_bits_registrador(endereco)
        print(f"Estado do Bit 6 após escrita: {bits[6]}")
        
        print("Aguardando 2 segundos (observe a mudança de vazão no terminal do servidor)...")
        sleep(2)
        print("\nDesativando bit 6 (Desabilitar sistema)...")
        cliente.escrever_bit_individual(endereco, 6, 0)
        bits = cliente.ler_bits_registrador(endereco)
        print(f"Estado do Bit 6 final: {bits[6]}")
        
        cliente.desconectar()
    else:
        print("Falha na conexão com o servidor.")

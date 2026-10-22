import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cliente.cliente_modbus import ClienteMODBUS
from time import sleep

if __name__ == "__main__":
    cliente = ClienteMODBUS('localhost', 502)
    if cliente.conectar():
        print("--- Demonstração Float e Escala ---")
        
        tensao_regs = cliente.ler_holding_register(847)
        if tensao_regs:
            val_num = tensao_regs[0]
            val_eng = val_num * 0.1
            print(f"Tensão R-S lida: Valor Numérico = {val_num}, Div = 10, Engenharia = {val_eng:.1f} V")
        
        setpoint_eng = 25.5
        print(f"\nEscrevendo Setpoint: {setpoint_eng} L/min (Float32)")
        cliente.escrever_float32(1302, setpoint_eng)
        
        sleep(0.5)
        sp_lido = cliente.ler_float32(1302)
        if sp_lido is not None:
            print(f"Setpoint Lido do Servidor: {sp_lido:.4f}")
        
        cliente.desconectar()
    else:
        print("Falha na conexão com o servidor.")

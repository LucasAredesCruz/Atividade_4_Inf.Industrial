# Atividade Prática ENE118: Comunicação Modbus TCP com Emulação de CLP

## Integrantes
- [Nome do Integrante 1] - Implementação do servidor, lógica de simulação.
- [Nome do Integrante 2] - Implementação do cliente, funções de conversão e exemplos.

## Execução
1. Crie o ambiente virtual: `python -m venv .venv` e ative-o (`.venv\Scripts\activate` no Windows).
2. Instale as dependências: `pip install -r requirements.txt`.
3. Em um terminal, inicie o servidor: `python servidor/servidor_modbus.py`
4. Em outro terminal, execute os testes: 
   `python exemplos/exemplo_float.py`
   `python exemplos/exemplo_bits.py`

## Mapa de Registradores
Servidor escuta em `localhost:502`. Ordem de palavras (Word Order) para floats (FP): Big Endian.

| Tag | Tipo | Endereços | Div | Mult | Unidade |
|---|---|---|---|---|---|
| bc.temp_r | Float32 | 700-701 | 10 | 0,1 | °C |
| bc.temp_s | Float32 | 702-703 | 10 | 0,1 | °C |
| bc.temp_t | Float32 | 704-705 | 10 | 0,1 | °C |
| bc.temp_carc | Float32 | 706-707 | 10 | 0,1 | °C |
| bc.pit01 | Float32 | 710-711 | 1 | 1 | bar |
| bc.fit01 (Vazão) | Float32 | 712-713 | 1 | 1 | L/min |
| bc.frequencia | Inteiro | 830 | 100 | 0,01 | Hz |
| bc.corrente_r | Inteiro | 840 | 10 | 0,1 | A |
| bc.tensao_rs | Inteiro | 847 | 10 | 0,1 | V |
| bc.fp_r | Inteiro | 868 | 1000 | 0,001 | - |
| bc.sp_pid | Float32 | 1302-1303 | 1 | 1 | L/min |
| bc.habilita | Bit | 1328 | - | - | Bit 6 |

**Comportamento da Simulação:** O bit 6 do registrador 1328 habilita o sistema. Quando ativo (1), a medição da vazão persegue o setpoint. Quando desativado (0), a vazão decai exponencialmente para zero.

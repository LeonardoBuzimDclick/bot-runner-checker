import psutil
import subprocess
import os
import datetime
import time

PROCESSO = ["ElectroNeek-loader.exe", "ElectroNeek Bot Runner", "ElectroNeek Bot Runner.exe"]
CAMINHO_EXE = r"C:\Program Files\ElectroNeek Robot\Loader\ElectroNeek-loader.exe"


def programa_esta_rodando(nomes_processos):
    for processo in psutil.process_iter(['pid', 'name']):
        if processo.info['name'].lower() in [p.lower() for p in nomes_processos]:
            return True
    return False

def processo_esta_realmente_ativo(nomes_processos):
    registrar_log_erro("iniciando")
    for processo in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        if processo.info['name'] in nomes_processos:
            # Espera um momento e pega o uso de CPU novamente
            time.sleep(1)
            cpu_uso = processo.cpu_percent(interval=1)
            
            if cpu_uso > 0:  # Se estiver usando CPU, então está realmente ativo
                registrar_log_erro("Retornando true")
                
                return True
    registrar_log_erro("Retornando false")
    return False

def registrar_log_erro(mensagem):
    data_atual = datetime.datetime.now().strftime('%Y-%m-%d')
    hora_atual = datetime.datetime.now().strftime('%H-%M-%S')
    pasta_log = os.path.join("logs", data_atual)
    os.makedirs(pasta_log, exist_ok=True)
    caminho_log = os.path.join(pasta_log, f"log_{hora_atual}.txt")
    
    with open(caminho_log, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ERRO: {mensagem}\n")


def registrar_historico(registro):
    with open("Historico.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(registro)


def registrar_ultima_execucao(status):
    with open("Ultima_execucao.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Ativo - Status: {status}\n")


def executar_como_admin(caminho_exe):
    try:
        registrar_log_erro("Iniciando executar")
        
        #subprocess.run([caminho_exe], check=True)
        subprocess.run(["powershell", f'Start-Process "{caminho_exe}"'], shell=True, check=True)
        #subprocess.run(["runas", "/user:Administrador", caminho_exe], shell=True, check=True)
        registrar_log_erro("pos executar")
        registrar_historico(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Ativado\n")
        registrar_ultima_execucao("Iniciado")
    except subprocess.CalledProcessError as e:
        registrar_log_erro(f"Erro ao iniciar o programa: {e}")
    except Exception as e:
        registrar_log_erro(f"Erro inesperado: {e}")


if not programa_esta_rodando(PROCESSO):
#if not processo_esta_realmente_ativo(PROCESSO):
    registrar_historico(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Inativo\n")
    executar_como_admin(CAMINHO_EXE)
else:
    registrar_ultima_execucao("Em execução")

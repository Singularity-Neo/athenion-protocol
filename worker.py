import asyncio
import websockets
import json
import random
import time
import psutil
import threading
import os
from pystray import MenuItem, Menu, Icon
from PIL import Image
from transformers import pipeline
import torch
from solders.keypair import Keypair

# ========================= CONFIGURAÇÕES =========================
DISPATCHER_URI = "ws://127.0.0.1:8765"
MAX_CPU_THRESHOLD = 0.20
CHECK_INTERVAL = 10
MALICIOUS_PROB = 0.0  # 0.0 para testes limpos → consenso sempre 100%
MODEL_NAME = "gpt2"  # Modelo leve (~1.2-1.8 GB RAM por worker)
# =================================================================

running = threading.Event()
running.set()
pause_event = threading.Event()
worker_id = None
generator = None
worker_keypair = Keypair()

# Persistência da wallet (mesmo wallet toda vez que o worker roda)
WALLET_FILE = "worker_wallet.json"
if os.path.exists(WALLET_FILE):
    with open(WALLET_FILE, "r") as f:
        secret = json.load(f)
        worker_keypair = Keypair.from_bytes(bytes(secret))
else:
    with open(WALLET_FILE, "w") as f:
        json.dump(list(worker_keypair.to_bytes()), f)

pubkey = str(worker_keypair.pubkey())

def load_model():
    global generator
    if generator is None:
        print("Carregando GPT-2 (leve – primeira vez pode demorar ~1-2 min para download)...")
        generator = pipeline("text-generation", model=MODEL_NAME, device=-1)  # CPU only
        torch.manual_seed(42)  # Determinismo total
        print("GPT-2 carregado com sucesso!")

def is_system_idle():
    if psutil.cpu_percent(interval=0.1) / 100.0 > MAX_CPU_THRESHOLD:
        return False
    return True

async def worker_loop():
    global worker_id
    load_model()
    while running.is_set():
        if pause_event.is_set():
            await asyncio.sleep(1)
            continue

        if not is_system_idle():
            await asyncio.sleep(CHECK_INTERVAL)
            continue

        try:
            async with websockets.connect(DISPATCHER_URI) as ws:
                # Registro inicial
                msg = await ws.recv()
                data = json.loads(msg)
                if data["type"] == "registered":
                    worker_id = data["worker_id"]
                    await ws.send(json.dumps({
                        "type": "pubkey",
                        "worker_id": worker_id,
                        "pubkey": pubkey
                    }))
                    print(f"Conectado ao Dispatcher | ID: {worker_id} | Wallet: {pubkey[:8]}...")

                # Loop de mensagens
                async for message in ws:
                    data = json.loads(message)
                    if data["type"] == "task":
                        prompt = data["prompt"]
                        max_tokens = data["max_tokens"]
                        print(f"\nIniciando inferência GPT-2:\n'{prompt[:100]}...' (+{max_tokens} tokens)")

                        # Inferência determinística (greedy)
                        output = generator(
                            prompt,
                            max_new_tokens=max_tokens,
                            do_sample=False,
                            temperature=0.0
                        )[0]['generated_text']

                        generated = output.strip()

                        # Simulação maliciosa (desativada por padrão)
                        if random.random() < MALICIOUS_PROB:
                            generated = "MALICIOUS OUTPUT - INVALID INFERENCE " + str(random.randint(1, 100000))
                            print("[SIMULAÇÃO] Worker malicioso ativado")

                        result = {
                            "type": "result",
                            "worker_id": worker_id,
                            "task_id": data["task_id"],
                            "generated_text": generated
                        }
                        await ws.send(json.dumps(result))
                        print("Resultado enviado ao Dispatcher")

                    elif data["type"] == "consensus":
                        print(f"\n=== Consenso Final Recebido ===\nConfiança: {data['confidence']:.1f}%\nTexto: {data['generated_text'][:300]}...\n")

                    elif data["type"] == "reward_tx":
                        print(f"\n=== Recompensa $GENKI Recebida (Devnet)! ===\nTransaction Signature: {data['signature']}\nLink Explorer: https://explorer.solana.com/tx/{data['signature']}?cluster=devnet")

        except (websockets.ConnectionClosed, ConnectionRefusedError, Exception) as e:
            print(f"Dispatcher indisponível ou erro: {e}. Reconectando em 10s...")
            await asyncio.sleep(10)

# System tray (controle fácil pelo usuário)
def setup_tray():
    image = Image.new('RGB', (64, 64), (0, 255, 0))
    menu = Menu(
        MenuItem('Pause' if not pause_event.is_set() else 'Resume', toggle_pause),
        MenuItem('Exit', stop_agent)
    )
    icon = Icon("GenkiAgent", image, "Genki Worker - Sovereign Swarm (GPT-2)", menu)
    return icon

def toggle_pause(icon, item):
    if pause_event.is_set():
        pause_event.clear()
        icon.title = "Genki Worker - Running"
    else:
        pause_event.set()
        icon.title = "Genki Worker - Paused"
    icon.update_menu()

def stop_agent(icon, item):
    running.clear()
    icon.stop()
    os._exit(0)

if __name__ == "__main__":
    print("Genki Worker Agent v5.0 - GPT-2 Leve + Sovereign Swarm Active")
    thread = threading.Thread(target=lambda: asyncio.run(worker_loop()), daemon=True)
    thread.start()
    icon = setup_tray()
    icon.run()
import asyncio
import websockets
import json
import uuid
import random
from collections import Counter
from solders.keypair import Keypair  # <-- Import corrigido
from solders.pubkey import Pubkey   # <-- Se precisar (usado implicitamente via str)

# ========================= CONFIGURAÇÕES =========================
HOST = "127.0.0.1"
PORT = 8765
MIN_WORKERS_FOR_TASK = 3
PROMPT = "The Sovereign Swarm of the Athenion Protocol represents the future of decentralized collective intelligence because"
MAX_TOKENS = 30
MALICIOUS_SIMULATION = 0.2
REWARD_AMOUNT_LAMPORTS = 1000
# =================================================================

connected_workers = {}  # {worker_id: {"ws": ws, "pubkey": str}}
results = {}

async def register(websocket):
    worker_id = str(uuid.uuid4())
    connected_workers[worker_id] = {"ws": websocket, "pubkey": None}
    await websocket.send(json.dumps({"type": "registered", "worker_id": worker_id}))
    print(f"Worker registrado: {worker_id} | Total: {len(connected_workers)}")

    if len([w for w in connected_workers.values() if w["pubkey"]]) >= MIN_WORKERS_FOR_TASK:
        await start_distributed_task()

async def unregister(worker_id):
    if worker_id in connected_workers:
        del connected_workers[worker_id]
    print(f"Worker desconectado | Restantes: {len(connected_workers)}")

async def start_distributed_task():
    print("\n=== Iniciando tarefa de inferência distribuída (Vital Energy) ===")
    task = {
        "type": "task",
        "task_id": str(uuid.uuid4()),
        "prompt": PROMPT,
        "max_tokens": MAX_TOKENS
    }
    
    results.clear()
    results["task_id"] = task["task_id"]
    results["outputs"] = {}

    for worker_id, info in connected_workers.items():
        if info["pubkey"]:
            await info["ws"].send(json.dumps(task))

async def handle_worker(websocket):
    await register(websocket)
    worker_id = None
    try:
        async for message in websocket:
            data = json.loads(message)
            if data["type"] == "pubkey":
                worker_id = data["worker_id"]
                pubkey = data["pubkey"]
                if worker_id in connected_workers:
                    connected_workers[worker_id]["pubkey"] = pubkey
                print(f"Worker {worker_id} registrou wallet: {pubkey}")
                if len([w for w in connected_workers.values() if w["pubkey"]]) >= MIN_WORKERS_FOR_TASK:
                    await start_distributed_task()

            elif data["type"] == "result":
                task_id = data["task_id"]
                generated_text = data["generated_text"]
                worker_id = data["worker_id"]

                results["outputs"][worker_id] = generated_text
                print(f"Resultado recebido de {worker_id}: {generated_text[:60]}...")

                if len(results["outputs"]) == len([w for w in connected_workers.values() if w["pubkey"]]):
                    await finalize_consensus(task_id)
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        if worker_id:
            await unregister(worker_id)

async def finalize_consensus(task_id):
    counter = Counter(results["outputs"].values())
    consensus_text, votes = counter.most_common(1)[0]
    total = len(results["outputs"])
    confidence = votes / total * 100

    print("\n=== Proof-of-Inference Consensus ===")
    print(f"Texto consenso: {consensus_text}")
    print(f"Confiança: {confidence:.1f}% ({votes}/{total} workers)")

    honest_workers = [wid for wid, text in results["outputs"].items() if text == consensus_text]
    print(f"Recompensando {len(honest_workers)} workers honestos com {REWARD_AMOUNT_LAMPORTS} lamports de $GENKI cada:")
    for wid in honest_workers:
        pubkey = connected_workers[wid]["pubkey"]
        print(f"  → Worker {wid} ({pubkey[:8]}...): +{REWARD_AMOUNT_LAMPORTS} lamports (Vital Energy)")

    final_msg = {
        "type": "consensus",
        "generated_text": consensus_text,
        "confidence": confidence
    }
    if connected_workers:
        await asyncio.gather(*(info["ws"].send(json.dumps(final_msg)) for info in connected_workers.values() if info["pubkey"]))

async def main():
    print(f"Dispatcher (Rainha) iniciada em ws://{HOST}:{PORT}")
    async with websockets.serve(handle_worker, HOST, PORT):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
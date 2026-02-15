import multiprocessing
import random
import time
from collections import Counter

NUM_WORKERS = 10
MALICIOUS_RATIO = 0.2
TASK_SAMPLES = 1_000_000

def honest_worker(seed):
    random.seed(seed)
    inside = sum(1 for _ in range(TASK_SAMPLES) if random.random()**2 + random.random()**2 <= 1)
    return 4 * inside / TASK_SAMPLES

def malicious_worker(seed):
    return round(random.uniform(2.0, 4.0), 5)  # resultado errado

def worker_task(worker_id, seed, result_queue):
    time.sleep(random.uniform(0.5, 2.0))  # simula latência
    if random.random() < MALICIOUS_RATIO:
        result = malicious_worker(seed)
        print(f"Worker {worker_id} (malicious) returned {result}")
    else:
        result = honest_worker(seed)
        print(f"Worker {worker_id} (honest) returned {result}")
    result_queue.put((worker_id, result))

if __name__ == "__main__":
    print("=== Athenion Protocol - Proof-of-Inference Consensus PoC ===\n")
    seed = 12345
    manager = multiprocessing.Manager()
    result_queue = manager.Queue()

    processes = []
    for i in range(NUM_WORKERS):
        p = multiprocessing.Process(target=worker_task, args=(i, seed, result_queue))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    results = [result_queue.get()[1] for _ in range(NUM_WORKERS)]
    consensus = Counter(results).most_common(1)[0]
    print("\n=== Consensus Result ===")
    print(f"Consensus value: {consensus[0]:.6f} (votes: {consensus[1]}/{NUM_WORKERS})")
    print(f"Confidence: {consensus[1]/NUM_WORKERS*100:.1f}%")
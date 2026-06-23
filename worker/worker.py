import redis
import json
import uuid
import sys
from tasks import TASK_REGISTRY

class DistributedWorker:
    def __init__(self, queue_name="distributed_task_queue", host="localhost", port=6379):
        self.queue_name = queue_name
        # Connect directly to our running local Redis server
        self.redis_client = redis.Redis(host=host, port=port, decode_responses=True)
        self.worker_id = str(uuid.uuid4())[:8]

    def start(self):
        print("==================================================================")
        print(f"BOOTING RUNTIME DAEMON: WORKER_ID [{self.worker_id}] ONLINE")
        print("==================================================================")
        print(f"Listening gracefully to broker channel '{self.queue_name}'...\n")

        try:
            while True:
                # BRPOP blocks the execution thread until an item drops into the list.
                # This guarantees 0% CPU consumption while the queue is completely empty.
                job = self.redis_client.brpop(self.queue_name, timeout=0)
                
                # job looks like: ("distributed_task_queue", '{"task_id": "...", ...}')
                raw_payload = job[1]
                payload = json.loads(raw_payload)

                task_id = payload.get("task_id")
                task_name = payload.get("task_name")
                args = payload.get("args", [])

                print(f"[Event] Picked up Job ID [{task_id}] -> Executing target: '{task_name}'")

                if task_name not in TASK_REGISTRY:
                    error_msg = f"Task execution rejected: '{task_name}' not registered."
                    print(f"[ERROR] {error_msg}")
                    self.redis_client.hset(f"result:{task_id}", mapping={"status": "FAILED", "error": error_msg})
                    continue

                try:
                    # Dynamically invoke the function pointer using our lookup dictionary
                    execution_target = TASK_REGISTRY[task_name]
                    output = execution_target(*args)

                    # Store the complete operational outcome metrics securely inside a Redis Hash
                    self.redis_client.hset(f"result:{task_id}", mapping={
                        "status": "SUCCESS",
                        "output": str(output),
                        "executed_by": self.worker_id
                    })
                    print(f"[Success] Job ID [{task_id}] calculated cleanly. Results pushed to state database.\n")

                except Exception as e:
                    print(f"[CRITICAL ERROR] Execution failed: {str(e)}")
                    self.redis_client.hset(f"result:{task_id}", mapping={"status": "FAILED", "error": str(e)})

        except KeyboardInterrupt:
            print(f"\n[Shutdown] Worker daemon [{self.worker_id}] gracefully terminating connections. Goodbye.")
            sys.exit(0)

if __name__ == "__main__":
    worker = DistributedWorker()
    worker.start()
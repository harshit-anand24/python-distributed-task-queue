import redis
import json
import uuid
import time

class TaskQueueClient:
    def __init__(self, queue_name="distributed_task_queue", host="localhost", port=6379):
        self.queue_name = queue_name
        self.redis_client = redis.Redis(host=host, port=port, decode_responses=True)

    def delay(self, task_name, *args):
        """Asynchronously dispatches a task to the message broker matrix."""
        task_id = str(uuid.uuid4())
        payload = {
            "task_id": task_id,
            "task_name": task_name,
            "args": args
        }
        
        # Serialize to a standard network transmission JSON string and append to list
        self.redis_client.lpush(self.queue_name, json.dumps(payload))
        print(f"[Client] Dispatched: '{task_name}' with args {args}. Task signed as ID [{task_id}]")
        return task_id

    def get_result(self, task_id, block=False, timeout=10):
        """Polls or monitors the result state hash matrix inside Redis."""
        start_time = time.time()
        while True:
            result = self.redis_client.hgetall(f"result:{task_id}")
            if result:
                return result
            if not block or (time.time() - start_time > timeout):
                return None
            time.sleep(0.5)

if __name__ == "__main__":
    print("==================================================================")
    # Instantiate the application tracking interface
    client = TaskQueueClient()
    print("BOOTING APP SERVER WORKLOAD DISPATCHER")
    print("==================================================================\n")

    # 1. Fire off an intensive CPU calculation request
    id_one = client.delay("compute_factorial", 50)
    
    # 2. Fire off a structural string reversal processing layout
    id_two = client.delay("transform_data_payload", "   systems engineering optimization validation   ")

    print("\n[Client] Non-blocking dispatch pass clear! Main application loop remains completely unblocked.")
    print("[Client] Polling cluster network for background task completion state updates...")

    # Wait and track the outcomes
    for name, tid in [("Factorial", id_one), ("String Transformation", id_two)]:
        outcome = client.get_result(tid, block=True, timeout=5)
        print(f"\n>>> Async Metrics for {name} Task:")
        print(json.dumps(outcome, indent=4))
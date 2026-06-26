import redis
import json
import uuid
import time

class DistributedTaskClient:
    def __init__(self, queue_name="distributed_task_queue", host="localhost", port=6379):
        self.queue_name = queue_name
        self.redis_client = redis.Redis(host=host, port=port, decode_responses=True)

    def delay(self, task_name, *args):
        """
        Pushes a task signature onto the distributed Redis queue list.
        Generates a unique transaction task_id for tracking.
        """
        task_id = str(uuid.uuid4())
        payload = {
            "task_id": task_id,
            "task_name": task_name,
            "args": list(args)
        }
        # Right-push the JSON string representation of our task payload
        self.redis_client.lpush(self.queue_name, json.dumps(payload))
        return task_id

    def get_result(self, task_id, block=True, timeout=10):
        """
        Polls or checks the Redis state hash for execution completion metrics.
        """
        start_time = time.time()
        key_name = f"result:{task_id}"

        while True:
            # Check if our result hash exists
            result = self.redis_client.hgetall(key_name)
            if result:
                return result

            if not block:
                return None

            # Timeout safety guardrail
            if time.time() - start_time > timeout:
                return {"status": "TIMEOUT", "error": f"Task execution exceeded {timeout} seconds limit."}

            time.sleep(0.1) # Soft sleep to prevent CPU thrashing during local polling loops


if __name__ == "__main__":
    print("==================================================================")
    print("BOOTING APP SERVER WORKLOAD DISPATCHER")
    print("==================================================================")

    client = DistributedTaskClient()

    # =====================================================================
    # TASK DISPATCH STAGE (Non-blocking Network Submissions)
    # =====================================================================
    
    # 1. Fire off an intensive CPU calculation request (Image Optimization)
    print("[Client] Dispatching: 'optimize_image_payload'...")
    id_one = client.delay("optimize_image_payload", "profile_pic.png", 800, 90)
    
    # 2. Fire off a styled system transactional validation email dispatch
    print("[Client] Dispatching: 'send_automated_email'...")
    id_two = client.delay("send_automated_email", "harshit@example.com", "Security Verification Required", "Harshit Anand", "VERIFY_99A")

    # 3. Fire off an asynchronous API Web Data Aggregator request
    print("[Client] Dispatching: 'fetch_and_aggregate_api_data'...")
    id_three = client.delay("fetch_and_aggregate_api_data")

    # 4. Fire off structured database dataset serialization to a CSV flat file
    print("[Client] Dispatching: 'export_raw_data_to_csv'...")
    mock_dataset = [
        {"id": "101", "name": "Harshit Anand", "role": "Systems Architect", "active_nodes": "4"},
        {"id": "102", "name": "Production Worker A", "role": "GPU Crunch Node", "active_nodes": "12"},
        {"id": "103", "name": "Production Worker B", "role": "I/O API Fetcher", "active_nodes": "8"},
        {"id": "104", "name": "Redis Cluster Agent", "role": "Broker Queue", "active_nodes": "1"}
    ]
    id_four = client.delay("export_raw_data_to_csv", "infrastructure_report.csv", mock_dataset)

    print("\n[Client] Non-blocking dispatch pass clear! Main application loop remains completely unblocked.")
    print("[Client] Polling cluster network for background task completion state updates...")

    # =====================================================================
    # RESULTS TRACKING STAGE (Blocking Metrics Collection)
    # =====================================================================
    tasks_to_track = [
        ("Image Optimization", id_one),
        ("Automated Verification Email", id_two),
        ("API Analytics Aggregation", id_three),
        ("Structured CSV Exporter", id_four)
    ]

    for name, tid in tasks_to_track:
        # We increase the timeout to 10 seconds to allow for network / mock image overhead
        outcome = client.get_result(tid, block=True, timeout=10)
        print(f"\n>>> Async Metrics for {name} Task (ID: {tid}):")
        
        # Check if the output string is a nested stringified JSON dictionary so we can print it prettily
        if outcome.get("output"):
            try:
                outcome["output"] = json.loads(outcome["output"].replace("'", '"'))
            except Exception:
                pass # Leave as plain string if it isn't JSON formatting
                
        print(json.dumps(outcome, indent=4))
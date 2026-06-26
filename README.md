# Pluggable Distributed Task Queue Matrix (Asynchronous Worker Engine)

A high-performance, decoupled asynchronous task distribution architecture built from scratch in Python and backed by Redis for centralized message-broker synchronization and shared state metrics storage.

## Structural Architecture
* **Non-Blocking Client Dispatch:** Leverages Redis primitives to offload intensive compute payloads instantly, allowing client main threads to maintain $O(1)$ reactivity while long-running jobs are safely queued.
* **Efficient Daemon Polling:** Uses atomic blocking operations (`BRPOP`) inside isolated background workers to enforce 0% CPU consumption during idle cluster phases.
* **Centralized Shared State Matrix:** Utilizes Redis Hashes to maintain real-time task completion statistics, dynamic traceback tracking, and node execution attribution logs.

### Advanced Cluster Network Execution Logs

```text
=== WINDOW 1: APP SERVER WORKLOAD DISPATCHER ===
Last login: Fri Jun 26 13:17:39 on ttys000
(base) harshitanand@Harshits-MacBook-Air-2 client % python app.py 
==================================================================
BOOTING APP SERVER WORKLOAD DISPATCHER
==================================================================
[Client] Dispatching: 'optimize_image_payload'...
[Client] Dispatching: 'send_automated_email'...
[Client] Dispatching: 'fetch_and_aggregate_api_data'...
[Client] Dispatching: 'export_raw_data_to_csv'...

[Client] Non-blocking dispatch pass clear! Main application loop remains completely unblocked.
[Client] Polling cluster network for background task completion state updates...

>>> Async Metrics for Image Optimization Task (ID: ffd98951-086e-40ce-b8b1-b5f8b8970b5f):
{
    "output": {
        "status": "SUCCESS",
        "message": "Successfully optimized and filtered image frame.",
        "metrics": {
            "saved_filepath": "optimized_profile_pic.png",
            "new_dimensions": "800x450",
            "compression_quality": "90%",
            "file_size_bytes": 6638
        }
    },
    "executed_by": "e1c999a3",
    "status": "SUCCESS"
}

>>> Async Metrics for Automated Verification Email Task (ID: 96bf0bb9-5103-4095-b2f4-487d56b5e06e):
{
    "output": {
        "status": "SANDBOX_VERIFIED",
        "message": "Mail processed and recorded in local dispatch logs.",
        "delivery_recipient": "harshit@example.com",
        "smtp_payload_preview": {
            "from": "system-daemon@sandbox-cluster.io",
            "to": "harshit@example.com",
            "subject": "Security Verification Required",
            "content_type": "text/html"
        }
    },
    "executed_by": "6cc18159",
    "status": "SUCCESS"
}

>>> Async Metrics for API Analytics Aggregation Task (ID: 0bce128d-7ee9-4f8f-b774-f086f0689c32):
{
    "output": {
        "status": "SUCCESS",
        "source_endpoint": "https://jsonplaceholder.typicode.com/posts",
        "analytics": {
            "parsed_records_count": 100,
            "unique_active_users_detected": 10,
            "average_words_per_title": 6.13,
            "most_active_contributor_id": 1,
            "processing_timestamp": 1782465540.16997
        }
    },
    "executed_by": "e1c999a3",
    "status": "SUCCESS"
}

>>> Async Metrics for Structured CSV Exporter Task (ID: cdce760c-cf5c-4f89-b1c5-850d413025c5):
{
    "output": {
        "status": "SUCCESS",
        "target_file": "infrastructure_report.csv",
        "metrics": {
            "compiled_rows": 4,
            "column_headers": [
                "id",
                "name",
                "role",
                "active_nodes"
            ],
            "file_size_bytes": 187
        }
    },
    "executed_by": "e1c999a3",
    "status": "SUCCESS"
}
```

```text
=== WINDOW 2: RUNTIME DAEMON - WORKER_ID [e1c999a3] ===
Last login: Fri Jun 26 14:36:36 on ttys001
(base) harshitanand@Harshits-MacBook-Air-2 worker % python worker.py
==================================================================
BOOTING RUNTIME DAEMON: WORKER_ID [e1c999a3] ONLINE
==================================================================
Listening gracefully to broker channel 'distributed_task_queue'...

[Event] Picked up Job ID [ffd98951-086e-40ce-b8b1-b5f8b8970b5f] -> Executing target: 'optimize_image_payload'
[Image Task] Processing image: profile_pic.png
[Image Task] File profile_pic.png not found. Creating a temporary mock canvas...
[Success] Job ID [ffd98951-086e-40ce-b8b1-b5f8b8970b5f] calculated cleanly. Results pushed to state database.

[Event] Picked up Job ID [0bce128d-7ee9-4f8f-b774-f086f0689c32] -> Executing target: 'fetch_and_aggregate_api_data'
[Analytics Task] Querying remote datastore endpoint: https://jsonplaceholder.typicode.com/posts
[Analytics Task] Fetched 100 data structures. Running aggregation formulas...
[Success] Job ID [0bce128d-7ee9-4f8f-b774-f086f0689c32] calculated cleanly. Results pushed to state database.

[Event] Picked up Job ID [cdce760c-cf5c-4f89-b1c5-850d413025c5] -> Executing target: 'export_raw_data_to_csv'
[Export Task] Processing raw tabular array into file: infrastructure_report.csv
[Success] Job ID [cdce760c-cf5c-4f89-b1c5-850d413025c5] calculated cleanly. Results pushed to state database.
```

```text
=== WINDOW 3: RUNTIME DAEMON - WORKER_ID [6cc18159] ===
Last login: Fri Jun 26 14:38:48 on ttys005
(base) harshitanand@Harshits-MacBook-Air-2 worker % python worker.py
==================================================================
BOOTING RUNTIME DAEMON: WORKER_ID [6cc18159] ONLINE
==================================================================
Listening gracefully to broker channel 'distributed_task_queue'...

[Event] Picked up Job ID [96bf0bb9-5103-4095-b2f4-487d56b5e06e] -> Executing target: 'send_automated_email'
[Email Task] Generating HTML template payload for harshit@example.com...
[Email Task] [SANDBOX MODE] Simulating network latency...
[Success] Job ID [96bf0bb9-5103-4095-b2f4-487d56b5e06e] calculated cleanly. Results pushed to state database.
```
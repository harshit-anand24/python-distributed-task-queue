# Pluggable Distributed Task Queue Matrix (Asynchronous Worker Engine)

A high-performance, decoupled asynchronous task distribution architecture built from scratch in Python and backed by Redis for centralized message-broker synchronization and shared state metrics storage.

## Structural Architecture
* **Non-Blocking Client Dispatch:** Leverages Redis primitives to offload intensive compute payloads instantly, allowing client main threads to maintain $O(1)$ reactivity while long-running jobs are safely queued.
* **Efficient Daemon Polling:** Uses atomic blocking operations (`BRPOP`) inside isolated background workers to enforce 0% CPU consumption during idle cluster phases.
* **Centralized Shared State Matrix:** Utilizes Redis Hashes to maintain real-time task completion statistics, dynamic traceback tracking, and node execution attribution logs.

### Terminal Workspace Execution Logs

````text
==================================================================
BOOTING APP SERVER WORKLOAD DISPATCHER
==================================================================

[Client] Dispatched: 'compute_factorial' with args (50,). Task signed as ID [5d5550f5-b8b0-4854-9797-06b1300156f6]
[Client] Dispatched: 'transform_data_payload' with args ('   systems engineering optimization validation   ',). Task signed as ID [4f0edbe7-1c6b-43f9-8d8a-77f5a12147d7]

[Client] Non-blocking dispatch pass clear! Main application loop remains completely unblocked.
[Client] Polling cluster network for background task completion state updates...

>>> Async Metrics for Factorial Task:
{
    "status": "SUCCESS",
    "output": "304140932017133780436126081660...",
    "executed_by": "61fae969"
}

>>> Async Metrics for String Transformation Task:
{
    "status": "SUCCESS",
    "output": "NOITADILAV NOITAZIMITPO GNIREENIGNE SMETSYS",
    "executed_by": "a22eb0c4"
}
```

```text
==================================================================
BOOTING RUNTIME DAEMON: WORKER_ID [a22eb0c4] ONLINE
==================================================================
Listening gracefully to broker channel 'distributed_task_queue'...

[Event] Picked up Job ID [4f0edbe7-1c6b-43f9-8d8a-77f5a12147d7] -> Executing target: 'transform_data_payload'
[Computation] Cleaning and mutating raw string payload...
[Success] Job ID [4f0edbe7-1c6b-43f9-8d8a-77f5a12147d7] calculated cleanly. Results pushed to state database.
```

```text
==================================================================
BOOTING RUNTIME DAEMON: WORKER_ID [61fae969] ONLINE
==================================================================
Listening gracefully to broker channel 'distributed_task_queue'...

[Event] Picked up Job ID [5d5550f5-b8b0-4854-9797-06b1300156f6] -> Executing target: 'compute_factorial'
[Computation] Executing factorial calculation for n=50...
[Success] Job ID [5d5550f5-b8b0-4854-9797-06b1300156f6] calculated cleanly. Results pushed to state database.
```
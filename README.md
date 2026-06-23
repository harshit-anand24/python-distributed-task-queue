# Pluggable Distributed Task Queue Matrix (Asynchronous Worker Engine)

A high-performance, decoupled asynchronous task distribution architecture built from scratch in Python and backed by Redis for centralized message-broker synchronization and shared state metrics storage.

## Structural Architecture
* **Non-Blocking Client Dispatch:** Leverages Redis primitives to offload intensive compute payloads instantly, allowing client main threads to maintain $O(1)$ reactivity while long-running jobs are safely queued.
* **Efficient Daemon Polling:** Uses atomic blocking operations (`BRPOP`) inside isolated background workers to enforce 0% CPU consumption during idle cluster phases.
* **Centralized Shared State Matrix:** Utilizes Redis Hashes to maintain real-time task completion statistics, dynamic traceback tracking, and node execution attribution logs.

## Cluster Execution Logs
```text
=== WINDOW 1: WORKER DAEMON RUNTIME ===
==================================================================
BOOTING RUNTIME DAEMON: WORKER_ID [c9acae63] ONLINE
==================================================================
Listening gracefully to broker channel 'distributed_task_queue'...

[Event] Picked up Job ID [05f1e9d8-3390-4adc-b93c-3ae745c9411d] -> Executing target: 'compute_factorial'
[Computation] Executing factorial calculation for n=50...
[Success] Job ID [05f1e9d8-3390-4adc-b93c-3ae745c9411d] calculated cleanly.

=== WINDOW 2: CLIENT WORKLOAD INTERFACE ===
>>> Async Metrics for Factorial Task:
{
    "status": "SUCCESS",
    "output": "304140932017133780436126081660...",
    "executed_by": "c9acae63"
}
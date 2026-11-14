# Architecture

```mermaid
flowchart LR
  Input[Diff or local Git repository] --> D[Diff Agent\nparse + change analysis]
  D <--> S[(Shared ChangeState)]
  S --> A[Style Agent]
  S --> B[Security Agent]
  S --> C[Test-Coverage Agent]
  A --> S
  B --> S
  C --> S
  S --> M[Reviewer Manager\naggregate + decision]
  M --> R[JSON/UI report + append-only log]
```

After the Diff Agent, `asyncio.gather` fans work out to three independent specialist coroutines (plus the completed diff specialist), which write findings under a lock to `ChangeState`. The Reviewer Manager fans results in, deduplicates them, and applies the deterministic policy. Semantic Kernel supplies the real `Kernel` and per-agent registered callable plugin objects; offline mode deliberately invokes the registered analysis implementations locally, without an LLM or submitted-code execution.

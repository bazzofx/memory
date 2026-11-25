# Agent Learning & Reflection Policy

## Purpose

Continuously improve software development quality, execution efficiency, reliability and agent capabilities through structured memory and evidence-based improvement proposals.

The agent must distinguish between temporary problems, reusable lessons and opportunities for lasting improvement.

## 1. Core Principles

- Prioritise completing the user's assigned task.
- Prefer evidence over speculation.
- Preserve knowledge that will benefit future tasks.
- Avoid storing trivial, redundant or temporary information.
- Learn from failures and successful approaches.
- Identify recurring inefficiencies without endlessly repeating unsuccessful solutions.
- Never treat an improvement proposal as permission to change the environment.
- Minimise unnecessary context consumption.

## 2. When to Create a Memory

Create or update a memory when an experience provides reusable knowledge.

### Worth Remembering

**Failures and troubleshooting**
- A non-obvious bug was identified and resolved.
- An error revealed an important dependency or compatibility limitation.
- A recurring failure was traced to a root cause.
- A workaround was verified.

**Successful approaches**
- A technique produced a measurable improvement.
- A reusable solution was validated.
- A debugging strategy significantly reduced investigation time.

**Architecture and decisions**
- An important design decision was made.
- A technology was selected or rejected for a documented reason.
- A trade-off affects future development.

**Environment and procedures**
- A useful environment-specific constraint was discovered.
- A reliable development, testing or deployment procedure was established.

### Do Not Remember

- Simple typos or routine syntax corrections.
- Temporary logs without lasting significance.
- Information already adequately documented.
- Speculative solutions presented as proven.
- Repeated descriptions of the same issue.
- Secrets, credentials or sensitive data unnecessarily.

### Memory Storage

Classify each memory into the appropriate category:

- `issues.md`
- `successes.md`
- `decisions.md`
- `preferences.md`
- `environments.md`
- `procedures.md`
- `limitations.md`
- `pending.md`

Before writing:
1. Search for an existing related memory.
2. Update or merge when appropriate.
3. Preserve evidence, context and the verified outcome.
4. Assign a unique identifier.
5. Update the lightweight memory index.
6. Avoid loading unrelated categories.

## 3. When to Consider Creating a Dream

A dream represents a potentially valuable improvement to the agent's tools, capabilities, workflows, development practices or execution environment.

### Trigger A: Repeated Failure

Consider a dream when:
- The same approach fails approximately three times without meaningful progress.
- Existing workarounds repeatedly prove ineffective.
- The agent repeatedly encounters a class of errors that could be prevented automatically.

Before proposing a dream, consider whether changing the troubleshooting approach would resolve the problem immediately.

Example: Propose an automated API compatibility checker after repeated schema-related failures across tasks.

### Trigger B: Performance Bottleneck

Consider a dream when:
- An operation is consistently slower than an established baseline.
- Previous optimisations have failed to deliver adequate improvement.
- Repetitive operations consume significant execution time or tokens.
- A promising alternative could produce measurable benefits.

Example: Benchmark a streaming parser against the current file-processing implementation.

### Trigger C: Missing Capability

Consider a dream when:
- The agent lacks a useful testing, analysis or debugging tool.
- A repetitive manual operation could become a reusable utility.
- An integration could eliminate recurring workflow friction.

Example: Propose a dependency-auditing utility for recurring compatibility investigations.

### Trigger D: Software Quality

Consider a dream when:
- Similar bugs repeatedly escape testing.
- A missing test framework or validation mechanism creates recurring problems.
- Repetitive code could be replaced by a reusable abstraction.
- An automated quality gate could prevent recurring mistakes.

### Trigger E: Knowledge or Architecture

Consider a dream when:
- The current approach repeatedly conflicts with project requirements.
- A new technique warrants a bounded experiment.
- Evidence suggests a simpler, more reliable architecture.

## 4. Dream Qualification

Evaluate candidates using:

- **Frequency:** How often has the issue occurred?
- **Impact:** How much time, cost, quality or reliability does it affect?
- **Actionability:** Is there a specific improvement to investigate?
- **Reusability:** Would it benefit multiple future tasks?
- **Evidence:** Are there observations supporting the proposal?

Prefer proposals that are measurable and reusable.

A high-impact one-off issue may qualify without recurring.

Reject weak proposals that merely rephrase a memory or lack an actionable improvement.

## 5. Troubleshooting Before Dreaming

When repeated attempts fail:

1. Stop repeating substantially identical actions.
2. Inspect error messages, assumptions and available evidence.
3. Change the troubleshooting strategy.
4. Consult relevant existing memories.
5. Escalate genuine blockers to the user when necessary.
6. Record a dream only if a reusable capability improvement is justified.

A dream must not replace the responsibility to troubleshoot the current task.

## 6. End-of-Task Reflection

After meaningful tasks:

1. Identify new lessons and observations.
2. Run Memory Optimizer.
3. Classify, merge and save reusable knowledge.
4. Send newly created or meaningfully updated memories to Dream Manager.
5. Prioritise Issues, Successes and Limitations.
6. Check existing dreams before proposing another.
7. Create or update dreams when justified.
8. Record the originating memory identifiers and evidence.

Do not duplicate task-level reflection at session end unless new evidence exists.

## 7. Dream Lifecycle

Proposed → Approved Experiment → Testing → Awaiting Implementation Approval → Implemented

Alternative states:
- Deferred
- Rejected
- Abandoned

Dreams must have:
- Unique identifier
- Problem or opportunity
- Supporting evidence
- Proposed improvement
- Expected benefit
- Validation method
- Related memory identifiers
- Current status

Experiments, installations, access requests, significant code changes and deployments must respect the user's approval and permission boundaries.

## 8. Session Behaviour

At the beginning of a recognised new session:

- Load the minimal global context and memory index.
- Retrieve relevant memories for the current work.
- Present up to three valuable pending dreams when appropriate.
- Avoid repeating previously rejected or unchanged proposals.
- Do not interrupt urgent or explicitly focused work with dream reviews.

## 9. Success Criteria

The system should produce:

- Fewer repeated mistakes.
- Faster troubleshooting.
- Lower unnecessary context consumption.
- More reusable tools and workflows.
- Better software quality.
- Fewer duplicate memories and dreams.
- Measurable improvement from approved experiments.

The goal is not to maximise memory or dream creation.

**The goal is to improve future work while storing as little unnecessary information as possible.**
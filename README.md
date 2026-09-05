# Codex-Agent-Lab

A lightweight research and evaluation framework for coding agents that inspect repositories, execute tests, plan repairs, modify code, and validate fixes through iterative feedback.

The project focuses on **coding-agent reliability, trajectory analysis, and repair evaluation** rather than benchmark accuracy alone.

---

## Overview

Codex-Agent-Lab studies how coding agents solve repository-level software repair tasks through an iterative agent loop:

1. Inspect the workspace
2. Run tests and collect execution evidence
3. Generate a repair plan
4. Apply a code modification
5. Re-run tests
6. Record the full agent trajectory
7. Continue until success or the iteration budget is exhausted

The goal is to make coding-agent behavior observable and measurable, including not only whether a task succeeds, but also **how the agent reaches the solution**.

---

## Agent Architecture

The current agent follows an evidence-driven repair loop:

```text
                ┌──────────────────┐
                │   Coding Task    │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Inspect Workspace│
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │    Run Tests     │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Collect Evidence │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │  Repair Planner  │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │   Apply Repair   │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │  Re-run Tests    │
                └────────┬─────────┘
                         │
                  ┌──────┴──────┐
                  │             │
               PASS           FAIL
                  │             │
                  ▼             ▼
             Save Result   Next Iteration
                  │             │
                  │             └───────┐
                  │                     │
                  ▼                     │
           Record Trajectory ◄──────────┘

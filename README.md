# Applied AI Engineering

Lecture notes, teaching code, and shared student practice with Zohidjon.

Course topics: Python API → database → LLM integration → search and RAG → agents → evaluation → deployment. Learn the mechanism in Python, then explore its framework equivalent. The course project is still being decided and will be introduced in a later class; lesson examples are practice exercises.

## Start here

- [Setup](setup/README.md)
- [Student work and how to push](student-work/README.md)
- [Learning resources](resources/README.md)

## Lecture plan

The 12-week sequence below is a working outline. Dates and pacing can change. Exercises are informal: try things, save progress, ask questions, and learn together. No grading system or strict homework deadlines are configured.

| Week | Topic |
|---|---|
| 01 | [From Python script to API](lectures/week-01/README.md) |
| 02 | [PostgreSQL and persistent state](lectures/week-02/README.md) |
| 03 | [LLM calls, prompts, and structured results](lectures/week-03/README.md) |
| 04 | [Context, conversation memory, and streaming](lectures/week-04/README.md) |
| 05 | [Embeddings and search using linear algebra](lectures/week-05/README.md) |
| 06 | [pgvector and measured retrieval](lectures/week-06/README.md) |
| 07 | [RAG with citations and honest unknowns](lectures/week-07/README.md) |
| 08 | [Tool calling and a bounded agent](lectures/week-08/README.md) |
| 09 | [Translate the agent to LangGraph and integrate the harness](lectures/week-09/README.md) |
| 10 | [Evaluation, injection tests, and operating failures](lectures/week-10/README.md) |
| 11 | [Containerize and deploy](lectures/week-11/README.md) |
| 12 | [Verify independence and present evidence](lectures/week-12/README.md) |

## Where files go

```text
lectures/week-01/notes.md       Theory and explanations
lectures/week-01/code/         Instructor examples
lectures/week-01/exercises.md  Optional practice
student-work/<username>/      Student experiments and project links
resources/                    Reading and references
setup/                        Getting started
```

Lesson 1 now includes a student guide, theory notes, and a runnable FastAPI example. Later lecture notes and examples are being prepared; this is not a completed course implementation.

## Working together

The instructor maintains `lectures/`, `resources/`, and `setup/`. Students normally change only their own folder under `student-work/`. Suggestions and questions can be raised in Issues; pull requests are optional.

Repository collaborators with write access can technically edit all folders. Folder boundaries are a shared convention, not separate access controls. Everyone with repository read access can see student work.

Keep API keys and real `.env` files out of Git. Use `.env.example` with placeholders. Store large recordings elsewhere and add approved links instead.

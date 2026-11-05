# Lesson 1: Meet the group and build your first FastAPI service

We will meet each other, review the course topics and Git workflow, then turn familiar HTTP concepts into a running API. The course project will be introduced in a later class. Today's notes API is a small standalone exercise.

## Today's plan: 90 minutes

| Minutes | Activity |
|---|---|
| 0–7 | Instructor introduction: background, experience, and teaching approach |
| 7–20 | Student introductions: experience, what you can build, learning goals |
| 20–25 | Syllabus, weekly rhythm, and where materials and practice work live |
| 25–40 | Short Git/GitHub review and playground practice |
| 40–50 | Run FastAPI and send a request to `/health` |
| 50–65 | Create a note with POST and read it with GET |
| 65–80 | Add query filtering, inspect validation, and try failing requests |
| 80–87 | Make one independent change and commit your work |
| 87–90 | Explain one request and preview the next class |

## Introductions and course overview

Share your name, one thing you have built, what you can build independently, and what you want to learn. No separate Python basics exercise today.

The syllabus covers backend APIs, databases, model calls, context, retrieval, tools, evaluation, and deployment. The final project is still being decided. See the [course overview](../../README.md) for the topic sequence; its assistant example is provisional. Practice is informal, with no mandatory grades or fixed homework deadlines.

## Git and GitHub: save the work we are about to do

Git records project versions locally. GitHub hosts repositories for sharing them. The everyday cycle is **edit → stage → commit → push**. A commit stays local until you push it.

| Command | Purpose |
|---|---|
| `git status` | Inspect changed, staged, and untracked files |
| `git diff` | Inspect unstaged changes to tracked files |
| `git add <path>` | Select changes for a commit |
| `git commit -m "message"` | Save the staged snapshot locally |
| `git log --oneline` | Inspect commit history |
| `git clone <url>` | Get a first local copy |
| `git pull` / `git push` | Bring in remote work / send local commits |

Open [Coddy Git Playground](https://coddy.tech/playground/git) and replace its default script with:

```sh
git init
echo "Today I will build an API." > learning.md
git status
git add learning.md
git commit -m "Add lesson goal"
echo "An endpoint maps a method and path to a function." >> learning.md
git diff
git add learning.md
git commit -m "Record what an endpoint does"
git log --oneline
```

These are Linux playground commands. Every Run replays the complete script; use the step view to inspect intermediate states. The sandbox does not upload work to our real GitHub repository. Be ready to explain why the second edit needed another commit.

## Build the API in small steps

Follow the [setup and runnable example](code/README.md). Create your own `main.py` under `student-work/<your-username>/week-01/`. The completed instructor example lives in [code/main.py](code/main.py); keep it available to compare after trying a step.

### 1. A Python function becomes an endpoint

Start with only this:

```python
from fastapi import FastAPI

app = FastAPI(title="Our First API")

@app.get("/health")
def health():
    return {"status": "ok"}
```

Run the server. Open `http://127.0.0.1:8000/health`, then `http://127.0.0.1:8000/docs`. Change the returned JSON and send the request again.

Trace what actually happens: client sends GET `/health` → Uvicorn receives it → FastAPI matches the method and path → Python function runs → JSON response returns. The decorator registers a route; starting the server does not itself call the handler for a request.

### 2. Receive a JSON body and create a note

Add an in-memory `notes` list, the `NoteCreate` Pydantic model, and `POST /notes` from the instructor example. Use `/docs` → **Try it out** → **Execute** to send:

```json
{"title": "Learn FastAPI", "content": "I sent my first POST request."}
```

Inspect the method, URL, request body, response body, and `201` status. Explain where the generated ID comes from. Add `GET /notes` first as a simple `return notes`; retrieve the note you just created.

The browser address bar sends GET for this navigation. Use `/docs` to send a POST request with a body. GET and POST can share `/notes` because method plus path identifies the operation.

### 3. Query parameters and validation

Extend `list_notes` with the optional `q` parameter and title filtering shown in the completed example. Create two notes, then try `/notes?q=fastapi`. Compare a query parameter in the URL with the JSON body used by POST.

Run these experiments:

| Request | Expected observation |
|---|---|
| GET `/health` | `200`, status JSON |
| POST `/notes` with valid title | `201`, saved note with an ID |
| GET `/notes` | `200`, all notes created since startup/reload |
| GET `/notes?q=fastapi` | `200`, only titles containing that text, ignoring case |
| POST `/notes` with `{"title": ""}` | `422`, title length validation error |
| POST `/notes` with `{}` | `422`, required title missing |
| GET `/missing` | `404`, route not found |
| PUT `/notes` | `405`, method not allowed |

Use `/docs` for the defined routes. For the last two requests, use the PowerShell examples in the code guide. Predict each result before sending it. A `422` describes rejected input; it does not mean the Python server crashed.

Change code while using reload and observe that the notes disappear. Our list is temporary process memory. This exercise has no database; the in-memory ID strategy is only for a single-process teaching example.

## Your independent change

Choose one core task: add `GET /about` returning an API name and your name. Run it, inspect the JSON, and commit it in your own student-work folder. You do not need to finish every stretch task in the first class.

If you finish early, choose an [optional extension](exercises.md). Follow the [shared repository guide](../../student-work/README.md) when pushing. Stage only your own folder; leave the instructor example unchanged.

## Before you leave

Show one successful request and one rejected request. Explain which method/path selected the handler, where the input came from, and why the status was returned. Name one piece of state that will disappear when this server restarts.

The course project will be discussed next class. Further notes API work is practice, not a project commitment.

## References

- [FastAPI first steps and interactive docs](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [Request bodies with Pydantic](https://fastapi.tiangolo.com/tutorial/body/)
- [Query parameters](https://fastapi.tiangolo.com/tutorial/query-params/)

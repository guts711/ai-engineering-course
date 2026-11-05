# Lesson 1: Run the notes API

This is the completed reference for a small classroom exercise. Students build it incrementally in their own folder; it does not decide the course project.

## Windows / PowerShell

From your local course repository root, create an environment once:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r lectures/week-01/code/requirements.txt
```

Run the instructor example from the repository root:

```powershell
.venv\Scripts\python.exe -m uvicorn main:app --app-dir lectures/week-01/code --reload
```

To run your own work, stop that server with Ctrl+C and use your folder instead, replacing `your-username`:

```powershell
.venv\Scripts\python.exe -m uvicorn main:app --app-dir student-work/your-username/week-01 --reload
```

`main:app` means the `app` object in `main.py`. `--app-dir` tells Uvicorn where that file lives. Explicit interpreter paths avoid PowerShell activation-policy setup.

## macOS / Linux

From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r lectures/week-01/code/requirements.txt
.venv/bin/python -m uvicorn main:app --app-dir lectures/week-01/code --reload
```

Use `--app-dir student-work/your-username/week-01` for your own version.

## Send requests

Open `http://127.0.0.1:8000/docs`. Expand an operation, select **Try it out**, edit the input, and select **Execute**. Inspect the response status and JSON.

You can also use a second PowerShell terminal:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/notes -ContentType 'application/json' -Body '{"title":"Learn FastAPI","content":"My first POST"}'
Invoke-RestMethod http://127.0.0.1:8000/notes
Invoke-RestMethod 'http://127.0.0.1:8000/notes?q=fastapi'
```

The following deliberately return errors. In PowerShell 7, `-SkipHttpErrorCheck` lets you inspect them without an exception:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/missing -SkipHttpErrorCheck | Select-Object StatusCode, Content
Invoke-WebRequest -Method Put -Uri http://127.0.0.1:8000/notes -SkipHttpErrorCheck | Select-Object StatusCode, Content
```

Windows PowerShell 5.1 does not support that switch; use `curl.exe -i http://127.0.0.1:8000/missing` and `curl.exe -i -X PUT http://127.0.0.1:8000/notes` if curl is installed, or inspect the error's response status.

## What to notice

- `GET /health` returns a dictionary serialized as JSON.
- `GET /notes` reads data; optional `q` filters note titles.
- `POST /notes` validates a JSON body and returns `201` when it creates a note.
- Missing or empty titles return `422`. A whitespace-only title is currently accepted; stricter trimming is a possible extension.
- `notes` is a process-local list. Restarting, or a reload after a source edit, clears it. Multiple workers would have separate lists. This storage and ID strategy are for a classroom demonstration.

## Troubleshooting

- **Module not found:** use the environment's Python for installation and startup.
- **Could not import main:** run from the repository root and check `--app-dir`; the file must be named `main.py`.
- **Port 8000 already in use:** stop the previous server or add `--port 8001`, then use that port in URLs.
- **Cannot connect:** check that the terminal still shows a running server and use HTTP, not HTTPS.
- **Notes disappeared:** a server restart/reload clears the teaching list.
- **Docs UI does not load:** its assets require internet access by default. Use the terminal requests above if those assets are blocked.

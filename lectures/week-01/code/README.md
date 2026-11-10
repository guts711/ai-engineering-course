# Product Catalog references — setup, run, and test

These are completed teaching references for [Session 01](../session-01.md) and [Session 02](../session-02.md). Build incrementally during class. They are not the final AI project or production-ready shop software.

- `session01.py`: first-session stopping point, before the stock-field homework.
- `session02.py`: second-session reference including stock filters, output models, PUT, and DELETE.
- `test_main.py`: behavior checks for the Session 02 API.
- `requirements.txt`: pinned direct runtime dependencies.
- `requirements-dev.txt`: runtime dependencies plus test tools.

## Compare pure Python and Pydantic

Let's use only two fields: `name` and `price`. Read these files side by side:

- [Without Pydantic](pure_python_product.py): a function with ordinary `if` checks and `ValueError`.
- [With Pydantic](pydantic_product.py): a small model declaring the fields and constraints.

Both files run on their own. The [comparison script](compare_products.py) calls both using the same two values. After installing `requirements.txt`, run from the repository root:

```powershell
.venv\Scripts\python.exe lectures/week-01/code/compare_products.py
```

On macOS/Linux, use `.venv/bin/python` instead. No server or test framework is needed.

Start with `name = "Notebook"` and `price = 5`. Then change one value and rerun:

1. `price = -5`: both reject a negative price.
2. `price = "free"`: both reject a price they cannot use as a number.
3. `name = ""`: both reject an empty name.

The point is the code we had to write: the first version checks each rule manually; the second declares rules that Pydantic checks. These are introductory examples, not complete catalog validators. Pydantic also supports conversion: `price = "5"` becomes a number in this model, while our manual function rejects the string. We chose fewer features for the manual version so its checks stay readable.

There is no HTTP here. Pydantic raises `ValidationError` in Python; FastAPI adds the HTTP handling when we use a request model in an endpoint.

## Windows / PowerShell

Run these from the course repository root. Python 3.11+ is expected; the instructor verification environment uses Python 3.12. Avoid repeatedly recreating an existing environment.

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r lectures/week-01/code/requirements.txt
.venv\Scripts\python.exe -m uvicorn session01:app --app-dir lectures/week-01/code --reload
```

Open `http://127.0.0.1:8000/docs` and `/health`. Stop with Ctrl+C. For Session 02, run:

```powershell
.venv\Scripts\python.exe -m uvicorn session02:app --app-dir lectures/week-01/code --reload
```

For your own `main.py`, use `main:app` and replace `--app-dir` with `student-work/YOUR-USERNAME/week-01/catalog`. The explicit Python path avoids activation-policy problems.

To run the reference tests, first stop the server if desired (the tests do not need it):

```powershell
.venv\Scripts\python.exe -m pip install -r lectures/week-01/code/requirements-dev.txt
.venv\Scripts\python.exe -m pytest lectures/week-01/code/test_main.py -q
```

The root-relative `python -m pytest` invocation loads the test's adjacent `session02.py`. The fixture restores known data between tests. Do not run multiple independent test suites concurrently against the same imported in-memory module.

## macOS / Linux

From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r lectures/week-01/code/requirements-dev.txt
.venv/bin/python -m uvicorn session01:app --app-dir lectures/week-01/code --reload
# Stop with Ctrl+C, then switch references:
.venv/bin/python -m uvicorn session02:app --app-dir lectures/week-01/code --reload
# Tests do not require a running server:
.venv/bin/python -m pytest lectures/week-01/code/test_main.py -q
```

## Request checklist

Use `/docs` → operation → Try it out → Execute. Watch the response status/body and terminal log. PowerShell alternatives:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod 'http://127.0.0.1:8000/products?category=books&max_price=30'
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/products -ContentType 'application/json' -Body '{"name":"Notebook","price":5,"category":"stationery"}'
```

| Request | Session | Expected |
|---|---|---|
| GET `/products/1` | Both | 200, Python Handbook |
| GET `/products?category=BOOKS&max_price=30` | Both | 200, only product 1 |
| GET `/products/999` | Both | 404 |
| GET `/products/abc` or `/products/0` | Both | 422 |
| POST valid name/price/category | Both | 201, new server-generated ID |
| POST empty name or price 0 | Both | 422, no record created |
| GET `/products?in_stock=false` | Session 02 | 200, only product 3 in fresh seeds |
| PUT `/products/1` with all editable fields | Session 02 | 200, replacement with same ID |
| PUT without `in_stock` | Session 02 | 422 |
| DELETE `/products/1` | Session 02 | 204, empty body |
| GET deleted product | Session 02 | 404 |

Requests change state: restart before repeating checks that depend on seed records. Restart/reload restores three seeds and removes newly created products. Unknown extra inputs can be ignored under default Pydantic behavior; no `in_stock` support is claimed for Session 01.

## Common problems

- **Import error:** run from the repository root and check the filename and `--app-dir`.
- **Missing package:** install with the same environment's Python used for startup/tests.
- **Port in use:** stop the prior server or use `--port 8001` and change your request URLs.
- **Browser cannot connect:** check the server is running; use HTTP, not HTTPS.
- **`/docs` UI assets blocked:** try terminal requests instead; the default Swagger UI loads assets from an external CDN.
- **Unexpected reset:** editing Python while reload is enabled restarts the process.
- **TestClient deprecation warning:** the installed Starlette release may warn about its HTTPX backend. The pinned test setup is verified; students do not need to change clients during this lesson.

## Scope limits

One process, temporary dictionaries, demo float prices, no payments, security, persistent storage, or production concurrency guarantees. The output model removes a harmless demo `internal_note`; it is not an access-control system.

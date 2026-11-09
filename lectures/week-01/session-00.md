# Session 00: Introductions and development foundations

This recap covers our opening class: introductions, Git and GitHub, Python virtual environments and package management, and the HTTP request–response cycle. FastAPI implementation is reserved for a future session.

## 1. Introductions

We introduced ourselves and discussed our programming experience, what we can currently build, and what we want to learn. These conversations help shape the course pace and examples.

The course project has not been finalized. See the [course overview](../../README.md) for the working topic sequence. Practice is informal; questions and unfinished attempts are welcome.

## 2. Git and GitHub

**Git** tracks versions of files locally. **GitHub** hosts Git repositories so we can share code and collaborate. A repository contains the tracked project and its history.

The basic workflow is **edit → stage → commit → push**:

- Edit files in the working directory.
- Stage the changes you want in the next snapshot.
- Commit those staged changes with a useful message.
- Push local commits to GitHub so others can retrieve them.

| Command | Purpose |
|---|---|
| `git clone <url>` | Get a first local copy of a repository |
| `git status` | Inspect untracked, modified, and staged files |
| `git diff` | Inspect unstaged changes to tracked files |
| `git add <path>` | Stage changes at the selected path |
| `git commit -m "message"` | Record the staged snapshot locally |
| `git log --oneline` | View a compact history |
| `git pull` | Bring remote changes into your local branch |
| `git push` | Send local commits to the remote |

Saving a file is not the same as committing it. Committing is not the same as uploading it to GitHub. Also, `git diff` does not show the contents of untracked files; `git status` helps you spot them.

### Practice resource

[Coddy Git Playground](https://coddy.tech/playground/git) provides a place to practice without changing our course repository. Its Run button replays the complete script; use the step view to inspect the state after each command.

Optional review script for its Linux terminal:

```sh
git init
echo "Git records local project history." > learning.md
git status
git add learning.md
git commit -m "Add Git recap"
echo "GitHub hosts shared repositories." >> learning.md
git diff
git add learning.md
git commit -m "Explain GitHub"
git log --oneline
```

For real course work, follow the [student-work guide](../../student-work/README.md). Edit and stage your own folder. Keep environments and credentials out of Git.

## 3. Virtual environments and package management

A Python project often depends on external packages. Two projects may need different versions of the same package. A **virtual environment** gives a project its own Python environment and, by default, an isolated set of installed packages.

`venv` creates the environment. `pip` installs and manages packages for a Python interpreter. They have different jobs: an environment is where project packages live; a package installer puts packages there.

```text
Project A → .venv → its installed packages and versions
Project B → .venv → its installed packages and versions
```

Installing a package also installs required dependencies when needed. A requirements file describes packages to install; a line such as `package-name==1.2.3` requests a specific version.

### Reference commands: Windows / PowerShell

Run from your project directory:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip --version
.venv\Scripts\python.exe -m pip list
```

To install project dependencies when a requirements file is provided:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The filename is relative to your current directory; replace it with the actual file path. Using `.venv\Scripts\python.exe -m pip` explicitly selects that environment's Python and pip. `python -m pip` runs pip for whichever interpreter the `python` command selects.

### Activation and interpreter selection

Activation updates the current shell so commands such as `python` normally use the environment's interpreter. It does not create a new environment or install packages. In PowerShell, activate with `.\.venv\Scripts\Activate.ps1`. Run `deactivate` to leave an activated environment.

Activation is optional when you use the explicit interpreter path shown above. If activation is blocked by a local policy, use that path rather than changing your machine's policy for this exercise. Your editor must also use the intended interpreter.

On macOS/Linux, create the environment with `python3 -m venv .venv`, use `.venv/bin/python -m pip`, and activate with `source .venv/bin/activate` if desired.

### What belongs in Git?

Commit source code and dependency instructions such as `requirements.txt`. Do not commit `.venv/`, downloaded packages, or secrets. Each person recreates their own environment from the project instructions. A virtual environment isolates Python packages; it is not a separate operating system or security sandbox.

## 4. Request and response

A client sends an HTTP request to a server. The server processes it and returns an HTTP response. A browser, command-line tool, or Python program can act as a client.

```text
Client → request → server processes it → response → client
```

| Request contains | Response contains |
|---|---|
| Method, such as GET or POST | Status code, such as 200 or 404 |
| URL/path and optional query parameters | Headers describing the response |
| Headers describing the request | A body, when applicable |
| A body, when applicable | For example, JSON, HTML, or text |

Illustrative API exchange, not a service built during Session 00:

```http
GET /courses?topic=python HTTP/1.1
Host: example.com
Accept: application/json
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"courses": [{"title": "Python foundations"}]}
```

Here `/courses` is the path, `topic=python` is a query parameter, `200` is the response status, and the JSON is the response body. JSON is one possible format; not every response is JSON.

### Common HTTP methods

| Method | Typical API purpose |
|---|---|
| GET | Retrieve a resource or collection |
| POST | Submit data, often to create a resource |
| PUT | Replace a resource's representation |
| PATCH | Apply a partial update |
| DELETE | Remove a resource |

Method and path together select an API operation. A normal address-bar navigation sends a GET; sending a POST body usually needs a form, code, or an HTTP client. Status codes report outcomes: 2xx indicates success, 4xx a client-side/request problem, and 5xx a server-side problem.

## How these ideas connect

Git saves versions of our source code. GitHub shares them. A virtual environment holds the project's installed Python packages. A package installer installs the dependencies. When we run a server, clients communicate with it through requests and responses.

## Optional recap questions

1. What is the difference between saving a file, committing it, and pushing it?
2. Why might two Python projects need separate environments?
3. What is the difference between `venv` and `pip`?
4. How do you check which interpreter and pip you are using?
5. In an HTTP exchange, which parts belong to the request and which to the response?

Next, we can apply these foundations by implementing a small API with FastAPI. The [prepared example](code/README.md) is future practice, not a record of work completed in Session 00.

## References

- [Python virtual environments](https://docs.python.org/3/library/venv.html)
- [pip user guide](https://pip.pypa.io/en/stable/user_guide/)
- [Git practice](https://coddy.tech/playground/git)

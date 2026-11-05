# Lesson 1: Meet the group and make your first contribution

Today we get to know each other, look at what we will build, and use Git to save a small piece of work. You do not need to arrive knowing all the tools. Questions and unfinished attempts are welcome.

## Introduce yourself

Be ready to share your name, one thing you have built or changed, what you can do with Python now, and one thing you would like to build or learn.

## Where the course is going

We build one AI assistant in small steps:

1. A Python API and a database.
2. Model calls, conversation context, search, and answers grounded in documents.
3. Tools and a bounded agent, with a framework translation after the Python mechanism.
4. Evaluation, debugging, containers, and deployment.

See the [course overview](../../README.md). Practice is informal; there are no mandatory grades or fixed homework deadlines.

## A small Python activity

Predict the output before running this:

```python
topics = ["Python", "Git", "RAG"]

def find_topics(items, keyword):
    matches = []
    for item in items:
        if keyword.lower() in item.lower():
            matches.append(item)
    return matches

print(find_topics(topics, "g"))
```

Explain your prediction. Add `"Agents"` to the list. What changes? What happens if no topic matches? You can reason on paper if Python is not installed yet.

## Git and GitHub

Git tracks project versions on your computer. GitHub hosts repositories for sharing and collaboration.

| Action | Meaning |
|---|---|
| Edit | Change files in your working directory |
| `git status` | Inspect changed, staged, or untracked files |
| `git add <path>` | Select changes for the next commit |
| `git commit -m "message"` | Record the staged snapshot locally |
| `git log --oneline` | See a compact commit history |
| `git clone <url>` | Get a first local copy of a remote repository |
| `git pull` | Bring remote changes into your local branch |
| `git push` | Send local commits to the remote |

The basic cycle is **edit → stage → commit → push**. A local commit is not visible on GitHub until it is pushed.

## Practice in the playground

Open [Coddy Git Playground](https://coddy.tech/playground/git). Replace its sample with the script below. These commands are for the playground's Linux environment; they are not a Windows setup script.

```sh
git init
echo "I want to build an AI assistant." > introduction.txt
git status
git add introduction.txt
git status
git commit -m "Add my learning goal"
echo "I am learning how commits work." >> introduction.txt
git status
git add introduction.txt
git commit -m "Describe what I am learning"
git log --oneline
```

The playground replays the entire script each time you press Run. Use its step view to inspect the state after each command. This exercise stays in the sandbox; it does not upload anything to the course repository.

Try your own sentences and commit messages. Explain what changed between the two commits. Can you identify when the file was untracked, staged, and committed?

## Add your introduction to our repository

Follow the [student-work guide](../../student-work/README.md) and create:

```text
student-work/<your-github-username>/README.md
```

Use this short outline if helpful:

```markdown
# Hello, I am ...

## What I have tried

## What I can do now

## What I want to learn

## One project idea

## Something I would like help with
```

Commit your file with a message such as `Add my introduction`, then push it. Edit only your own folder. If access or installation is blocked, save the file locally and ask for help. You can use GitHub's web editor with write access while finishing local setup later.

## Before you leave

- Explain Git versus GitHub in one sentence.
- Explain what staging and committing did in your exercise.
- Share one thing you finished and one question you still have.

Optional practice: make one more small change and commit it. Next time, we will begin a small Python API, with setup or Python review first if needed.

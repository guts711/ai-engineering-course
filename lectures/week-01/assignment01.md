# Homework 01 — After Session 00

**Topic:** Git & GitHub fundamentals and HTTP review

**Due:** Before the next session

**Required:** Complete the video and the practical assignment below.

**Estimated time:** 60–90 minutes for the written/practical tasks, plus the video.

## Objective

Use Git and GitHub in a real development workflow: create a repository, track changes, commit code, push your work, and retrieve remote changes.

## 1. Watch the HTTP video

[Understanding HTTP for backend engineers, where it all starts](https://youtu.be/a3C1DMswClQ)

Watch this video before the next class.

## 2. Review the Session 00 topics

1. **Python package management:** What is `pip`, and why do we need package managers?
2. **Virtual environments:** Why do we use them? How do we create and activate one?
3. **HTTP requests and responses:** Review the client–server model, GET/POST/PUT/DELETE, and status codes 200, 404, and 500.

Be prepared to explain these concepts next session. You may be asked questions individually. See the [Session 00 notes](session-00.md) for reference.

## 3. Complete the Git & GitHub practical assignment

### Step 1: Create a repository

- Create a new **public** GitHub repository named `ai-engineering-practice`.
- Clone it to your computer using `git clone`.
- Open the cloned folder in VS Code.

### Step 2: Create the project files

```text
ai-engineering-practice/
├── README.md
├── main.py
└── .gitignore
```

- **README.md:** Write your name, the purpose of the repository, and what you learned in Session 00.
- **main.py:** Write a Python program that prints `Hello, AI Engineering!`.
- **.gitignore:** Add `.venv/`, `__pycache__/`, and `.env` so these files or folders are not tracked.

### Step 3: Commit and push

Use Git commands to:

1. Check the status of your files.
2. Stage your changes.
3. Create a commit with a meaningful message.
4. Push the changes to GitHub.

Verify that all three files appear in your GitHub repository.

### Step 4: Make another change

- Modify `main.py` to print your name as well.
- Check the differences using `git diff`.
- Create a second commit and push it to GitHub.

Your repository must contain **at least two commits**.

### Step 5: Practice pulling changes

- Edit `README.md` directly on GitHub and commit the change.
- Return to your terminal and use `git pull` to retrieve it.
- Verify that your local README contains the update.

## 4. Understand the commands

Be able to explain what each command does and when to use it:

```text
git clone
git status
git add
git commit
git push
git pull
git log
git diff
```

## 5. Prepare answers for next session

1. What is the difference between Git and GitHub?
2. What is the difference between `git add`, `git commit`, and `git push`?
3. What is the difference between `git pull` and `git clone`?
4. Why do we need `.gitignore`?
5. What is the difference between your local and remote repositories?

## Submission

Submit your **public repository URL before the next session**, through the channel specified by the instructor.

- The repository must be public.
- All three project files must be present.
- At least two commits must be visible.
- Your README must explain what you learned.

Understand every command you use. You may be asked to demonstrate the workflow next session.

This assignment uses your own repository; you do not need to copy the project into the shared course repository.

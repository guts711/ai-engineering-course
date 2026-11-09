# Upload and update homework

**Fork → edit → commit → push → pull request.** You push to your own copy; the instructor reviews and merges your work.

Replace `YOUR-USERNAME` with your GitHub username.

Follow each assignment's submission requirements first. [Homework 01](../lectures/week-01/assignment01.md) requires a separate public repository and submission of its URL; use this guide for work submitted to the shared course repository.

## 1. Set up once

Open [the course repository](https://github.com/zohidjon-m/ai-engineering-course) and click **Fork → Create fork**. Then run:

```powershell
git clone https://github.com/YOUR-USERNAME/ai-engineering-course.git
cd ai-engineering-course
git remote add upstream https://github.com/zohidjon-m/ai-engineering-course.git
```

Already cloned the instructor's repository? After creating your fork, run these inside your existing clone instead:

```powershell
git remote rename origin upstream
git remote add origin https://github.com/YOUR-USERNAME/ai-engineering-course.git
```

## 2. Start homework

Commit any current work before switching branches. Use a new branch name for each homework:

```powershell
git switch main
git fetch upstream
git merge --ff-only upstream/main
git switch -c homework/week-01
```

Create or edit files in `student-work/YOUR-USERNAME/week-01/`. Add a short README explaining what you tried, how to run it, and any questions.

## 3. Upload and submit

```powershell
git status
git add student-work/YOUR-USERNAME/
git commit -m "Add week 01 homework"
git push -u origin homework/week-01
```

On GitHub, open your fork and click **Compare & pull request**. Choose:

- **Base repository:** `zohidjon-m/ai-engineering-course`
- **Base branch:** `main`
- **Compare branch:** `homework/week-01` in your fork

Click **Create pull request**. The instructor will review and merge it.

## 4. Update the same homework

While its pull request is open, edit files on the same branch, then run:

```powershell
git add student-work/YOUR-USERNAME/
git commit -m "Update week 01 homework"
git push
```

The existing pull request updates automatically. After it is merged, repeat step 2 with a new branch for further changes.

Only edit your own folder. Never upload API keys, real `.env` files, or `.venv/`. Submitted work is visible to everyone with repository access. If a command fails, ask for help; do not force-push.

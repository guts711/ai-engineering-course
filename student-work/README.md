# Student work

A shared place for required practice, homework, questions, and project links. Complete assigned work and save it here or link your project as instructed. If you are blocked, share your progress, ask for help, and finish the task after resolving the issue.

Assignments are kept in their week’s folder. [Homework 01](../lectures/week-01/assignment01.md) requires a separate public repository and submission of its URL; follow that brief rather than copying its project into this shared folder.

## Your folder

Use your GitHub username:

```text
student-work/your-username/
  README.md
  week-01/
  week-02/
  projects/
```

Create only the folders you need. For a cumulative assistant project, keep one project in `projects/assistant/` and update it over time instead of copying it every week. You can also keep a separate personal repository and link it from your README.

In your README, describe what you completed, how to run it, the checks you performed, and any remaining blockers. Practice and homework are required; follow the instructor's submission instructions for each assignment.

## Save and push

The instructor must first give you write access. After cloning the course repository, run these commands from its root, replacing `your-username` with your actual username:

```powershell
git pull --rebase origin main
# Create or edit files inside student-work/your-username/.
git status
git add student-work/your-username/
git commit -m "Add my practice work"
git pull --rebase origin main
git push origin main
```

Pull before starting and again before pushing because this is a shared repository. Stage only your own folder. If Git reports a conflict, ask for help; do not force-push. No pull request is required for normal practice.

## Shared space

- Edit your own folder; ask before changing another student's work or lecture files.
- Everyone with repository access can read the work here. Folders do not provide private access.
- Keep keys, passwords, personal data, local environments, and large datasets out of Git.
- If you want feedback, open an Issue with a link to your file and a specific question.

# Student work

A shared place for experiments, optional homework, questions, and project links. Unfinished work is welcome.

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

In your README, briefly describe what you tried, how to run it, and anything you want help with. No fixed submission template, deadline, or grading is required.

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

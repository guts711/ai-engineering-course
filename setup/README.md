# Getting started

Install Git, Python 3.11 or later, and an editor such as VS Code. Create a GitHub account. The instructor will confirm the Python minor version and lesson dependencies before coding starts.

To upload homework, first fork this repository using the [student guide](../student-work/README.md), then clone your fork (replace `YOUR-USERNAME`):

```powershell
git clone https://github.com/YOUR-USERNAME/ai-engineering-course.git
cd ai-engineering-course
```

For Python exercises, create a local environment in your project folder:

```powershell
python -m venv .venv
.venv\Scripts\python.exe --version
```

Install dependencies only when the lecture or example provides its instructions. Later lessons will introduce Docker and PostgreSQL with their own setup guide. Model/provider configuration will be added when selected and tested by the instructor.

For pushing practice work and opening a pull request, follow [the student guide](../student-work/README.md). Push to your own fork; write access to the instructor's repository is not required. If the course repository is private, ask the instructor for access and confirm that forking is enabled.

# 100Hires-Project
This repository used as Portofolio Project given by 100Hires
## Tools Installed
* Cursor IDE
* Claude Code extension
* Codex extension
* Git for Windows

## Steps Completed
1. Downloaded and installed Cursor IDE.
2. Searched, installed, and successfully logged into the Claude Code extension.
3. Searched, installed, and successfully logged into the Codex extension.
4. Created a public GitHub repository.
5. Encountered a missing Git requirement, installed Git, and restarted the IDE.
6. Cloned the repository and opened it in Cursor IDE.
7. Created this README.md file to document the setup process.
8. Committed and pushed the changes to GitHub.

## Issues Encountered and Solutions
* **Issue:** When trying to clone the repository using the command palette in Cursor (`Ctrl+Shift+P`), the `Git: Clone` command did not appear. 
* **Solution:** I realized that Git was not installed on my Windows machine. I solved this by downloading and installing the 64-bit Git for Windows from the official website. After the installation was complete, I completely restarted Cursor IDE. The `Git: Clone` command then successfully appeared and functioned as expected.
* * **Issue 2:** When trying to make the first commit, I received an error stating `Make sure you configure your "user.name" and "user.email" in git.`
* **Solution 2:** I opened the integrated terminal in Cursor and configured my global Git identity using the `git config --global user.name` and `git config --global user.email` commands. After setting this up, the commit went through successfully.

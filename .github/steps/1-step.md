## Step 1: Enable Code Quality And Establish A Baseline

You are reviewing student complaints about missing enrollments, over-capacity registrations, and duplicate signups in the Mergington High activities site. Before fixing code, you need a trustworthy baseline that captures what the repository quality signals are reporting today.

### 📖 Theory: Why Start With A Baseline

Code Quality gives you maintainability and reliability findings directly in repository workflows.

- Enabling Code Quality on the repository starts analysis for the default branch.
- Findings can be filtered and triaged so teams can focus on the highest-risk problems first.
- A baseline issue creates a written artifact that can be referenced in future policy or audit conversations.

> [!NOTE]
> Code Quality scans consume GitHub Actions minutes. Review billing details here: https://docs.github.com/en/billing/concepts/product-billing/github-code-quality

Read more:

- https://docs.github.com/en/code-security/how-tos/maintain-quality-code
- https://docs.github.com/en/code-security/how-tos/maintain-quality-code/enable-code-quality
- https://docs.github.com/en/code-security/how-tos/maintain-quality-code/interpret-results

## ⌨️ Activity: (optional) Get to know the extracurricular activities site

Before we start developing and reviewing, let's take a moment to understand the current site.

> ❗ **Important:** Opening a development environment and running the application is **NOT** necessary to complete this exercise. You can skip this activity if desired.

1. Right-click the below button to open the **Create Codespace** page in a new tab. Use the default configuration.

   [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/{{full_repo_name}}?quickstart=1)

1. Wait some time for the environment to be prepared. It will automatically install all requirements and services.

1. Validate the **GitHub Copilot** and **Python** extensions are installed and enabled.

   <img width="300" alt="copilot extension for VS Code" src="https://github.com/user-attachments/assets/ef1ef984-17fc-4b20-a9a6-65a866def468" /><br/>
   <img width="300" alt="python extension for VS Code" src="https://github.com/user-attachments/assets/3040c0f5-1658-47e2-a439-20504a384f77" />

1. Try running the application. In the left sidebar, select the **Run and Debug** tab and then press the **Start Debugging** icon.

   <img width="300" alt="run and debug" src="https://github.com/user-attachments/assets/50b27f2a-5eab-4827-9343-ab5bce62357e" />

   <details>
   <summary>🤷 Having trouble?</summary><br/>

   If the **Run and Debug** area is empty, try reloading VS Code: Open the command palette (`Ctrl`+`Shift`+`P`) and search for `Developer: Reload Window`.

   <img width="300" alt="empty run and debug panel" src="https://github.com/user-attachments/assets/0dbf1407-3a97-401a-a630-f462697082d6" />

   </details>

1. Use the **Ports** tab to find the webpage address, open it, and verify it is running.

   <img width="350" alt="ports tab" src="https://github.com/user-attachments/assets/8d24d6b5-202d-4109-8174-2f0d1e4d8d44" />

   ![Screenshot of Mergington High School WebApp](https://github.com/user-attachments/assets/5e1e7c1e-1b0e-4378-a5af-a266763e6544)

### ⌨️ Activity: Enable Code Quality

1. In your repository, open the **Settings** tab.
1. In the left sidebar, find and select **Code quality**.
1. Select the **Enable** button.
1. Wait for the initial scan of the `main` branch to finish. This can take a few minutes.
1. In the top navigation, open the **Code quality** tab to see the findings.
1. Use the **Severity** filter and select `Error` to focus on the highest-risk findings.

<details>
<summary>Having trouble? 🤷</summary><br/>

- If findings are still loading, refresh the page after the initial scan completes.
- If you do not see the **Code quality** page, confirm your account has admin permissions on the repository.

</details>

### ⌨️ Activity: Start a baseline issue

Capturing a written baseline gives your team a reference point for future quality and audit conversations.

1. In the top navigation, open the **Issues** tab and select **New issue**.
1. Set the issue **title** to exactly:

   ```text
   Baseline code quality findings
   ```

1. Set the issue **description** to exactly the text below. The file list reflects the areas flagged in the sample project.

   ```text
   Severity: Error
   Rule: Commented-out code
   Files: src/backend/routers/activities.py, src/static/app.js, src/backend/routers/auth.py
   ```

1. Select **Create** to submit the issue.
1. Wait about 20 seconds, then refresh the page to see the results of the checks.

<details>
<summary>Having trouble? 🤷</summary><br/>

- Make sure the title matches exactly, with no extra spaces or punctuation.
- Make sure the description keeps the `Severity:`, `Rule:`, and `Files:` lines.

</details>

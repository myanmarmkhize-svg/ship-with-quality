## Step 1: Enable Code Quality And Preview Results

You are reviewing student complaints about missing enrollments, over-capacity registrations, and duplicate signups in the Mergington High activities site. Before fixing any code, you need to see what the repository's quality signals are reporting today.

### 📖 Theory: Insight Before Action

Code Quality gives you maintainability and reliability findings directly in your repository.

- Enabling Code Quality starts an analysis workflow on the default branch.
- Findings are grouped into **Standard findings** and **AI findings**, and can be filtered by severity or category.
- Reviewing findings first helps your team focus on the highest-risk problems before making changes.

> [!NOTE]
> Code Quality scans consume GitHub Actions minutes. Review billing details here: https://docs.github.com/en/billing/concepts/product-billing/github-code-quality

Read more:

- https://docs.github.com/en/code-security/how-tos/maintain-quality-code
- https://docs.github.com/en/code-security/how-tos/maintain-quality-code/enable-code-quality
- https://docs.github.com/en/code-security/how-tos/maintain-quality-code/interpret-results

## ⌨️ Activity: (optional) Get to know the extracurricular activities site

<details>
<summary>Show Steps</summary>

Before we start developing and reviewing, let's take a moment to understand the current site.

> ❗ **Important:** Opening a development environment and running the application is **NOT** necessary to complete this exercise. You can skip this activity if desired.

1. Right-click the below button to open the **Create Codespace** page in a new tab. Use the default configuration.

   [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/{{full_repo_name}}?quickstart=1)

1. Wait some time for the environment to be prepared. It will automatically install all requirements and services.

1. Validate the **Python** extensions is installed and enabled.

   <img width="300" alt="python extension for VS Code" src="images/vscode-python-extension.png" />

1. Try running the application. In the left sidebar, select the **Run and Debug** tab and then press the **Start Debugging** icon.

   <img width="300" alt="run and debug" src="images/run-and-debug.png" />

   <details>
   <summary>🤷 Having trouble?</summary><br/>

   If the **Run and Debug** area is empty, try reloading VS Code: Open the command palette (`Ctrl`+`Shift`+`P`) and search for `Developer: Reload Window`.

   <img width="300" alt="empty run and debug panel" src="images/run-and-debug-empty.png" />

   </details>

1. Use the **Ports** tab to find the webpage address, open it, and verify it is running.

   <img width="350" alt="ports tab" src="images/vscode-ports-tab.png" />

   ![Screenshot of Mergington High School WebApp](images/activity-site-preview.png)

</details>

## ⌨️ Activity: Enable Code Quality

1. Open another browser tab and navigate to this exercise repository.

1. In the top navigation, select the **Settings** tab.

   <img width="300px" alt="settings tab" src="images/settings-tab.png">

1. In the left sidebar, find and select **Code quality**.

   <img width="300px" alt="code quality section" src="images/left-nav-code-quality
   .png">

1. At the top of the page, select the **Enable** button.

   <img width="400px" alt="code quality enable button" src="images/code-quality-enable-button.png">

1. Wait for the initial scan of the default branch to finish. This can take a few minutes.

   > 💡 **Tip:** You can monitor progress by selecting the **Actions** tab in the top navigation.

   <img width="400px" alt="code quality first workflow" src="images/code-quality-first-workflow.png">

1. As the **Code Quality** analysis runs, Mona will detect it and prepare the next step. Continue to the next activity while the scan completes.

<details>
<summary>Having trouble? 🤷</summary><br/>

- If you do not see the **Code quality** option, your account may not have access to the feature. Please [check your availability](https://docs.github.com/en/code-security/concepts/about-code-quality#availability-and-usage-costs).
- If the scan does not start, refresh the settings page and confirm the **Enable** button was selected.

</details>

## ⌨️ Activity: Preview Results

Reviewing the initial findings gives your team a shared picture of what needs attention before making any code changes.

1. In the top navigation, select the **Security** tab.

1. In the left navigation, find the **Code quality** section and select **Standard findings**. Take a moment to review the results of this initial setup.

   <img width="400px" alt="standard findings" src="images/standard-findings.png">

1. Try using the **Filter** bar to search the list of findings, for example by **Severity** or **Category**.

   <img width="400px" alt="standard findings severity filter" src="images/standard-findings-filter-severity.png">

1. In the left navigation, find the **Code quality** section and select **AI findings**. These highlight issues that map to the reported student complaints.

   <img width="400px" alt="ai findings" src="images/ai-findings.png">

<details>
<summary>Having trouble? 🤷</summary><br/>

- If findings are still loading, refresh the page after the initial scan completes.
- If the **Security** tab shows nothing under **Code quality**, confirm the analysis workflow finished in the **Actions** tab.

</details>

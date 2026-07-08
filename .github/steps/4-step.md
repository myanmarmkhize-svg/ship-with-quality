## Step 4: Enforce Quality And Coverage With Rulesets

You now have quality findings and coverage data flowing on every pull request. The final step is turning those advisory signals into enforceable merge policy, exploring evaluate mode, and confirming that your fix satisfies the policy before merging.

### 📖 Theory: From Signals To Policy

Rulesets turn advisory checks into enforceable merge standards.

- Quality severity thresholds can block pull requests when unresolved findings exceed team limits.
- Coverage restrictions can prevent merges when coverage drops too far.
- **Evaluate mode** lets teams preview the impact of a ruleset without blocking merges. This is useful for understanding what would be blocked before fully committing to enforcement.
- Applying a ruleset in **Active** mode to an open pull request requires its checks to pass before the pull request can merge.

Read more:

- https://docs.github.com/en/code-security/how-tos/maintain-quality-code/set-pr-thresholds
- https://docs.github.com/en/code-security/how-tos/maintain-quality-code/restrict-code-coverage
- https://docs.github.com/en/code-security/how-tos/maintain-quality-code/unblock-your-pr
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets

### ⌨️ Activity: Enable Rulesets

1. In the top navigation, select the **Settings** tab.

   <img width="300" src="images/settings-tab.png">

1. In the left sidebar, expand **Rules** and select **Rulesets**.

   <img width="250" src="images/left-nav-rulesets.png">

1. Click the **New ruleset** button and select the **New branch ruleset** option.

   <img width="250" src="images/new-ruleset-button.png">

1. Use the following details and selected options.
   - **Ruleset Name**: `Quality and Coverage`
   - **Enforcement status**: `Active`
   - **Target branches**: `Include default branch`

1. Enable **Require code quality results**. Set the severity threshold to `Warnings and higher`.

   <img width="300" alt="rule to require code quality results" src="images/rulesets-require-coverage.png">

1. Enable **Restrict code coverage**. Set the **Minimum coverage percentage** to `60`.

   <img width="300" alt="rule to require code coverage" src="images/rulesets-restrict-code-coverage.png">

1. Scroll to the bottom and select **Create** to save the ruleset.

<details>
<summary>Having trouble? 🤷</summary><br/>

- Make sure the target includes the default branch (`main`).
- If checks are not evaluating later, confirm the enforcement status is correct.

</details>

### ⌨️ Activity: Switch To Evaluate Mode

Active enforcement is powerful, but sometimes teams want to understand the impact of a policy before fully committing to it. Evaluate mode logs what _would_ have been blocked, without actually preventing merges.

1. In the **Settings** tab, expand **Rules** in the left sidebar and select **Rulesets**.

1. Select the **Quality and Coverage** ruleset you just created.

1. Change the **Enforcement status** from `Active` to `Evaluate`.

1. Scroll to the bottom and select **Save changes**.

> 💡 **Tip:** In Evaluate mode, visit the **Insights** section under **Rules** in the left sidebar to see a log of what would have been blocked under Active enforcement, without any merges having been prevented.

<details>
<summary>Having trouble? 🤷</summary><br/>

- If you do not see the **Enforcement status** dropdown, make sure you opened the ruleset for editing (not just viewing).
- Confirm the change was saved by refreshing the page and checking the status shows `Evaluate`.

</details>

### ⌨️ Activity: Confirm Fixed Quality Issue And Merge

With the ruleset in Evaluate mode, let's confirm the quality fix is complete and merge the pull request.

1. Open the **Pull requests** tab and select your `fix-auth-quality-issues` pull request.

1. Wait for the Code Quality checks to finish on the pull request.

1. Confirm the quality findings for `auth.py` are resolved and no new issues were introduced.

   > 💡 **Tip:** If a check needs re-running, open the failed check to see which finding remains, fix it on the same branch, and commit again.

1. Once the checks complete, select **Merge pull request** and confirm.

1. Mona will detect the merge and wrap up the exercise.

<details>
<summary>Having trouble? 🤷</summary><br/>

- If a Code Quality finding remains, open the **AI findings** or **Standard findings** page to identify the remaining issue, fix it on the `fix-auth-quality-issues` branch, and commit again.
- Make sure your branch is named exactly `fix-auth-quality-issues` so the exercise can detect the merge.

</details>

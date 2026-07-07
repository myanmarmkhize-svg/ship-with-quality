## Step 2: Enable Code Coverage Analysis

After reviewing baseline findings, the principal asks how you know tests cover the risky paths. You now need pull-request coverage visibility so every change includes a test confidence signal.

### 📖 Theory: Coverage As A Merge Signal

Coverage complements static analysis by showing how much code is exercised by tests.

- Coverage files uploaded in Cobertura format can be surfaced in pull request context.
- Workflow permissions must allow writing code quality coverage data.
- Baseline branch runs plus pull request runs make comparisons meaningful.

Read more:

- https://docs.github.com/en/code-security/how-tos/maintain-quality-code/set-up-code-coverage
- https://docs.github.com/en/code-security/how-tos/maintain-quality-code/interpret-results
- https://github.com/actions/upload-code-coverage

### ⌨️ Activity: Upload test coverage

1. In your repository, open the **Code** tab and select the branch dropdown (it shows `main`).
1. In the **Find or create a branch** box, type `add-coverage-reporting` and select **Create branch: add-coverage-reporting from main**.
1. Open the test workflow file at `.github/workflows/tests.yml` and select the pencil (**Edit this file**) icon.
1. Replace the existing `permissions:` block with the block below. The `code-quality: write` permission is required to publish coverage results.

   ```yaml
   permissions:
     contents: read
     code-quality: write
   ```

1. Add the following step to the very end of the `steps:` list, directly below the "Run unit tests with coverage output" step. Keep the same indentation as the other steps.

   ```yaml
   - name: Upload coverage report to Code Quality
     uses: actions/upload-code-coverage@v1
     with:
       file: coverage.xml
       language: Python
       label: code-coverage/pytest
   ```

1. Select **Commit changes...**, keep **Commit directly to the `add-coverage-reporting` branch** selected, and confirm.
1. Open the **Pull requests** tab, select **New pull request**, set the base branch to `main` and the compare branch to `add-coverage-reporting`, then select **Create pull request** and confirm.
1. Wait about 20 seconds, then refresh the exercise issue to see the results of the checks. Once the workflow finishes, a coverage summary from `github-code-quality[bot]` also appears on the pull request.

<details>
<summary>Having trouble? 🤷</summary><br/>

- Confirm the "Run unit tests with coverage output" step still generates `coverage.xml`.
- Confirm the upload step uses `file: coverage.xml` and the workflow grants `code-quality: write`.

</details>

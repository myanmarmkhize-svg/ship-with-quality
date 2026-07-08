## Step 3: Enable Code Coverage

Findings from AI and standard analysis tell you about code quality, but they do not tell you how much of the code is actually tested. Code coverage fills that gap by showing which lines are exercised by your test suite on every pull request.

### 📖 Theory: Test Coverage As A Merge Signal

Test coverage complements static analysis by showing how much code is exercised by tests.

- Coverage uploaded in Cobertura format is surfaced in pull request context by `github-code-quality[bot]`.
- Workflow permissions must allow writing code quality coverage data (`code-quality: write`).
- Enabling coverage on the default branch means every new pull request automatically gets a coverage summary.

Read more:

- https://docs.github.com/en/code-security/how-tos/maintain-quality-code/set-up-code-coverage
- https://docs.github.com/en/code-security/how-tos/maintain-quality-code/interpret-results
- https://github.com/actions/upload-code-coverage

### ⌨️ Activity: Enable And Track Code Coverage

1. In your repository, open the **Code** tab and make sure you are on the `main` branch.

1. Open the test workflow file at `.github/workflows/tests.yml` and select the pencil (**Edit this file**) icon.

1. Update the existing `permissions:` block with the block below to include the `code-quality: write` permission, which allows publishing coverage results.

   ```yaml
   permissions:
     contents: read
     code-quality: write
   ```

1. Add the following step to the end of the `test` job, after the `Run unit tests with coverage output` step. Keep the same indentation as the other steps.

   ```yaml
   - name: Upload coverage report to Code Quality
     uses: actions/upload-code-coverage@v1
     with:
       file: coverage/coverage-python.xml
       language: Python
       label: code-coverage/pytest
   ```

1. Do the same for the `test-js` job, adding this step after its `Run unit tests with coverage output` step so the JavaScript coverage report is reported alongside the Python one.

   ```yaml
   - name: Upload coverage report to Code Quality
     uses: actions/upload-code-coverage@v1
     with:
       file: coverage/coverage-javascript.xml
       language: JavaScript
       label: code-coverage/jest
   ```

1. Commit your changes directly to the `main` branch. As soon as the coverage upload is committed, Mona will prepare the next step.

<details>
<summary>Having trouble? 🤷</summary><br/>

- Confirm the `Run unit tests with coverage output` step in `test` still generates `coverage/coverage-python.xml`, and the same step in `test-js` still generates `coverage/coverage-javascript.xml`.
- Confirm both upload steps use the correct `file:` path and `language:`, and that the workflow grants `code-quality: write`.
- You should see two coverage summaries from `github-code-quality[bot]`, one labeled `code-coverage/pytest` and one labeled `code-coverage/jest`.

</details>

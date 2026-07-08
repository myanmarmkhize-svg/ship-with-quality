## Step 2: Enable Code Coverage And Start Fixing A Quality Issue

The findings confirmed real defects behind the student complaints. Before you enforce anything, you want every pull request to show how well tests cover the code, and you will open your first remediation pull request.

### 📖 Theory: Test Coverage As A Merge Signal

Test coverage complements static analysis by showing how much code is exercised by tests.

- Coverage uploaded in Cobertura format is surfaced in pull request context by `github-code-quality[bot]`.
- Workflow permissions must allow writing code quality coverage data (`code-quality: write`).
- Enabling coverage on the default branch means every new pull request automatically gets a coverage summary.

Read more:

- https://docs.github.com/en/code-security/how-tos/maintain-quality-code/set-up-code-coverage
- https://docs.github.com/en/code-security/how-tos/maintain-quality-code/interpret-results
- https://github.com/actions/upload-code-coverage

## ⌨️ Activity: Enable and track code coverage

1. In your repository, open the **Code** tab and make sure you are on the `main` branch.

1. Open the test workflow file at `.github/workflows/tests.yml` and select the pencil (**Edit this file**) icon.

1. Update the existing `permissions:` block (line 27) with the block below, to include the `code-quality: write` permission, to allow publishing coverage results.

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

- Confirm the "Run unit tests with coverage output" step in `test` still generates `coverage/coverage-python.xml`, and the same step in `test-js` still generates `coverage/coverage-javascript.xml`.
- Confirm both upload steps use the correct `file:` path and `language:`, and that the workflow grants `code-quality: write`.
- You should see two coverage summaries from `github-code-quality[bot]`, one labeled `code-coverage/pytest` and one labeled `code-coverage/jest`.

</details>

## ⌨️ Activity: Start fixing a quality issue

The signup endpoint has three defects that match the reported problems. You will fix all three, add a test, and open a pull request so the coverage signal can appear.

- it never blocks duplicate signups
- it ignores the activity capacity
- it writes new signups to the wrong field.

1. Return to the **Code** tab of this exercise repo.

1. Create a branch with the name `fix-signup-validation-bugs`.

1. Open the file `src/backend/routers/activities.py`.

1. Search for the `signup_for_activity` function (line 67) and find the below unfinished code block:

   ```python
      # Validate student is not already signed up
      # if email in activity["participants"]:
      #     raise HTTPException(
      #         status_code=400, detail="Already signed up for this activity")

      # Add student to participants
      result = activities_collection.update_one(
         {"_id": activity_name},
         {"$push": {"participant": email}}
      )
   ```

1. Replace the incomplete code with the below corrected version:

   ```python
      # Validate the student is not already signed up
      if email in activity["participants"]:
         raise HTTPException(
            status_code=400, detail="Already signed up for this activity")

      # Validate the activity is not already at capacity
      if len(activity["participants"]) >= activity["max_participants"]:
         raise HTTPException(
            status_code=400, detail="This activity is already full")

      # Add student to participants
      result = activities_collection.update_one(
         {"_id": activity_name},
         {"$push": {"participants": email}}
      )
   ```

1. Open `tests/backend/routers/test_activities.py`, select the pencil icon, and add this test to the end of the file:

   ```python
   def test_signup_rejected_when_activity_is_full():
       # Description: This test verifies signup is rejected when the activity is at capacity.

       # Arrange
       client = _create_test_client_for_activities(
           {
               "Chess Club": {
                   "_id": "Chess Club",
                   "participants": ["existing@school.edu"],
                   "max_participants": 1,
                   "schedule_details": {
                       "days": ["Monday"],
                       "start_time": "15:15",
                       "end_time": "16:45",
                   },
               }
           },
           {"teacher1": {"_id": "teacher1"}},
       )

       # Act
       response = client.post(
           "/activities/Chess Club/signup",
           params={"email": "new@school.edu", "teacher_username": "teacher1"},
       )

       # Assert
       assert response.status_code == 400
   ```

1. Commit these changes to the `fix-signup-validation-bugs` branch with a message like `fix: signup validation`.

1. In the top navigation, select the **Pull requests** tab. Start a new pull request to merge your branch into main.
   - **base**: `main`
   - **compare**: `fix-signup-validation-bugs`

1. Wait about 20 seconds. Once the Code Quality analysis finishes, a coverage summary from `github-code-quality[bot]` appears as a comment on the pull request. You will use this pull request again in the next step.

<details>
<summary>Having trouble? 🤷</summary><br/>

- Make sure the branch is named exactly `fix-signup-validation-bugs`.
- If no coverage comment appears, confirm the coverage upload step was committed to `main` and that the Code Quality analysis completed in the **Actions** tab.

</details>

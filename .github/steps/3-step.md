## Step 3: Enforce Quality And Coverage With Rulesets

Visibility alone did not prevent risky code from merging under deadline pressure. In this step, you convert quality and coverage signals into branch policy and practice a real remediation flow.

### 📖 Theory: From Signals To Policy

Rulesets turn advisory checks into enforceable merge standards.

- Quality severity thresholds can block pull requests when unresolved findings exceed team limits.
- Coverage restrictions can prevent merges when coverage drops too far.
- Teams can move rulesets from `Active` to `Evaluate` to support a gradual rollout.

Read more:

- https://docs.github.com/en/code-security/how-tos/maintain-quality-code/set-pr-thresholds
- https://docs.github.com/en/code-security/how-tos/maintain-quality-code/restrict-code-coverage
- https://docs.github.com/en/code-security/how-tos/maintain-quality-code/unblock-your-pr
- https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-autofix
- https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets

### ⌨️ Activity: Create a quality enforcing ruleset

1. In your repository, open the **Settings** tab.
1. In the left sidebar, expand **Rules** and select **Rulesets**.
1. Select **New ruleset**, then **New branch ruleset**.
1. Set the **Ruleset Name** to `Quality and coverage`.
1. Set the **Enforcement status** to `Active`.
1. Under **Target branches**, select **Add target**, then **Include default branch**.
1. Under **Rules**, enable **Require code quality checks to pass** and set the severity threshold to `Error`.
1. Enable **Restrict code coverage** and set the minimum coverage threshold to `60%`.
1. Scroll to the bottom and select **Create** to save the ruleset.

<details>
<summary>Having trouble? 🤷</summary><br/>

- Make sure the target includes the default branch (`main`).
- If checks are not blocking later, confirm the enforcement status is `Active`.

</details>

### ⌨️ Activity: Fix a quality issue and merge

The signup endpoint has three defects that match the reported problems: it never blocks duplicate signups, it ignores the activity capacity, and it writes new signups to the wrong field. You will fix all three and add a test.

1. Open the **Code** tab, select the branch dropdown, type `fix-signup-validation-bugs`, and select **Create branch: fix-signup-validation-bugs from main**.
1. Open `src/backend/routers/activities.py` and select the pencil (**Edit this file**) icon.
1. Find this block inside the `signup_for_activity` function:

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

1. Replace that block with the corrected version below:

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

1. Select **Commit changes...**, keep **Commit directly to the `fix-signup-validation-bugs` branch** selected, and confirm.
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

1. Commit this change to the `fix-signup-validation-bugs` branch as well.
1. Open the **Pull requests** tab, select **New pull request**, set the base branch to `main` and the compare branch to `fix-signup-validation-bugs`, then create the pull request.
1. Because the ruleset is `Active`, the pull request cannot merge until the code quality and coverage checks pass. Wait for the checks to finish.
1. Once all checks pass, select **Merge pull request** and confirm.
1. Return to **Settings** → **Rules** → **Rulesets**, open `Quality and coverage`, change the **Enforcement status** from `Active` to `Evaluate`, and select **Save changes**.

<details>
<summary>Having trouble? 🤷</summary><br/>

- If a check still fails, open the failed check to see which finding remains, fix it, and commit again.
- Make sure your branch is named exactly `fix-signup-validation-bugs` so the exercise can detect the merge.

</details>

const fs = require("fs");
const path = require("path");

const INDEX_HTML_PATH = path.join(__dirname, "..", "..", "src", "static", "index.html");
const APP_JS_PATH = path.join(__dirname, "..", "..", "src", "static", "app.js");

// Flushes pending microtasks so async work inside app.js (fetch/json parsing) settles.
function flushPromises() {
  return new Promise((resolve) => setTimeout(resolve, 0));
}

// Loads a fresh copy of the DOM and app.js, mocking fetch with the given activities/session data.
async function loadApp({ activities = {}, currentUser = null } = {}) {
  document.documentElement.innerHTML = fs.readFileSync(INDEX_HTML_PATH, "utf8");
  window.localStorage.clear();
  if (currentUser) {
    window.localStorage.setItem("currentUser", JSON.stringify(currentUser));
  }

  global.fetch = jest.fn((url) => {
    if (String(url).startsWith("/auth/check-session")) {
      return Promise.resolve({ ok: true, json: () => Promise.resolve(currentUser) });
    }
    return Promise.resolve({ ok: true, json: () => Promise.resolve(activities) });
  });

  jest.resetModules();
  require(APP_JS_PATH);

  document.dispatchEvent(new window.Event("DOMContentLoaded", { bubbles: true, cancelable: true }));

  // Two ticks: one for the fetch() promise, one for the response.json() promise.
  await flushPromises();
  await flushPromises();
}

describe("activity rendering", () => {
  test("renders a card with the correct category tag for a sports activity", async () => {
    // Description: This test verifies an activity name containing "Soccer" is tagged as Sports.

    // Arrange
    const activities = {
      "Soccer Team": {
        description: "Competitive team practice",
        schedule_details: { days: ["Monday"], start_time: "15:00", end_time: "16:30" },
        max_participants: 20,
        participants: ["a@school.edu"],
      },
    };

    // Act
    await loadApp({ activities });

    // Assert
    const card = document.querySelector(".activity-card");
    expect(card.querySelector(".activity-tag").textContent.trim()).toBe("Sports");
  });

  test("shows a no-results message when no activities are returned", async () => {
    // Description: This test verifies the empty state is displayed when the activities list is empty.

    // Act
    await loadApp({ activities: {} });

    // Assert
    expect(document.querySelector(".no-results")).not.toBeNull();
    expect(document.querySelectorAll(".activity-card").length).toBe(0);
  });

  test("marks an activity as full and disables registration for authenticated teachers", async () => {
    // Description: This test verifies the register button is disabled once an activity is at capacity.

    // Arrange
    const activities = {
      "Chess Club": {
        description: "Weekly strategy sessions",
        schedule_details: { days: ["Monday"], start_time: "15:00", end_time: "16:00" },
        max_participants: 1,
        participants: ["existing@school.edu"],
      },
    };

    // Act
    await loadApp({ activities, currentUser: { username: "teacher1", display_name: "Teacher One" } });

    // Assert
    const registerButton = document.querySelector(".register-button");
    expect(registerButton).not.toBeNull();
    expect(registerButton.disabled).toBe(true);
    expect(registerButton.textContent.trim()).toBe("Activity Full");
  });
});

describe("filtering", () => {
  test("category filter hides activities that do not match the selected category", async () => {
    // Description: This test verifies clicking the Sports category filter hides non-sports activities.

    // Arrange
    const activities = {
      "Soccer Team": {
        description: "Competitive team practice",
        schedule_details: { days: ["Monday"], start_time: "15:00", end_time: "16:30" },
        max_participants: 20,
        participants: [],
      },
      "Debate Club": {
        description: "Academic competition practice",
        schedule_details: { days: ["Tuesday"], start_time: "15:00", end_time: "16:30" },
        max_participants: 20,
        participants: [],
      },
    };
    await loadApp({ activities });

    // Act
    document.querySelector('.category-filter[data-category="sports"]').dispatchEvent(new window.Event("click", { bubbles: true }));

    // Assert
    const cardNames = Array.from(document.querySelectorAll(".activity-card h4")).map((el) => el.textContent);
    expect(cardNames).toEqual(["Soccer Team"]);
  });

  test("search input filters activities by name", async () => {
    // Description: This test verifies typing into the search box filters the activity list by name.

    // Arrange
    const activities = {
      "Soccer Team": {
        description: "Competitive team practice",
        schedule_details: { days: ["Monday"], start_time: "15:00", end_time: "16:30" },
        max_participants: 20,
        participants: [],
      },
      "Debate Club": {
        description: "Academic competition practice",
        schedule_details: { days: ["Tuesday"], start_time: "15:00", end_time: "16:30" },
        max_participants: 20,
        participants: [],
      },
    };
    await loadApp({ activities });

    // Act
    const searchInput = document.getElementById("activity-search");
    searchInput.value = "debate";
    searchInput.dispatchEvent(new window.Event("input", { bubbles: true }));

    // Assert
    const cardNames = Array.from(document.querySelectorAll(".activity-card h4")).map((el) => el.textContent);
    expect(cardNames).toEqual(["Debate Club"]);
  });

  test("day filter click requests activities scoped to the selected day", async () => {
    // Description: This test verifies clicking a day filter re-fetches activities with a day query parameter.

    // Arrange
    await loadApp({ activities: {} });
    fetch.mockClear();

    // Act
    document.querySelector('.day-filter[data-day="Monday"]').dispatchEvent(new window.Event("click", { bubbles: true }));
    await flushPromises();
    await flushPromises();

    // Assert
    expect(fetch).toHaveBeenCalledWith(expect.stringContaining("day=Monday"));
  });
});

describe("authentication", () => {
  test("shows the logged-in teacher's display name after a valid session is restored", async () => {
    // Description: This test verifies a saved session restores the authenticated UI on load.

    // Act
    await loadApp({ activities: {}, currentUser: { username: "teacher1", display_name: "Teacher One" } });

    // Assert
    expect(document.getElementById("user-info").classList.contains("hidden")).toBe(false);
    expect(document.getElementById("display-name").textContent).toBe("Teacher One");
  });

  test("logout clears the authenticated state and shows the login button", async () => {
    // Description: This test verifies clicking logout restores the anonymous UI state.

    // Arrange
    await loadApp({ activities: {}, currentUser: { username: "teacher1", display_name: "Teacher One" } });

    // Act
    document.getElementById("logout-button").dispatchEvent(new window.Event("click", { bubbles: true }));

    // Assert
    expect(document.getElementById("login-button").classList.contains("hidden")).toBe(false);
    expect(document.getElementById("user-info").classList.contains("hidden")).toBe(true);
  });
});

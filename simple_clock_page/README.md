## Requirements

Implement a page with a clock. Design your solution according to the level specifications below (**current level is in bold**):

### Level 1
- The clock should be rendered with all functional elements (buttons, clock blocks, etc.).

### Level 2
- The rendered clock should support increasing and decreasing the hours and minutes.

To advance to the next level, you must pass all tests at the current level when submitting your solution.

---

## Level 1 Instructions

You are provided with a page containing a partial clock implementation. Your task is to render the missing buttons. The final result should look like this:

```html
<div id="ClockUpdater" class="container">
    <div class="row">
        <button id="hours-up-button">&uarr;</button>
        <button id="minutes-up-button">&uarr;</button>
    </div>

    <div class="row">
        <div id="clock"></div>
    </div>

    <div class="row">
        <button id="hours-down-button">&darr;</button>
        <button id="minutes-down-button">&darr;</button>
    </div>
</div>
```

> **Note:**  
> HTML element IDs are used for testing. Ensure you use the correct IDs, or your tests will not run correctly.

---

## Level 2 Instructions

You are given a page with a clock. Your task is to implement the logic for the buttons to increment and decrement the hours and minutes.

- The time should be displayed in **HH:MM** 24-hour format (e.g., `23:59`, `08:00`, `07:32`).
- The initial state of the clock should be `00:00`.
- Actions should cycle:  
    - If the clock shows `23:58` and you press the "hours up" button, the time should become `00:58`.
    - If the clock shows `00:00` and you press the "hours down" button, the time should become `23:00`.
- Hours and minutes should be changed independently using their respective buttons.

---

## Tests

- Unit tests are provided in `test/level<i>.test.js` for each level.
- To run tests, click the blue **Run** button. You can run tests in the Terminal or in a Structured manner.
- You may use `test/sample.test.js` to write your own tests, which will also be included in test runs.
- For debugging output in your tests, use the Terminal option for raw output.
- Debugging output from your application code can be found in your browser's console.
- For scored certifications, partial credit is granted for each unit test passed. Press **Submit** often to run tests and receive partial credits.

---

- **[Execution time limit]** 55 seconds
- **[Memory limit]** 4 GB

> If the question requires Front-End unit tests, a headless browser may be initialized for each test run, averaging ~20 seconds per run.
# QA Report: Island Height Guessing Game

## Bugs Identified, How They Were Noticed, and Fixes

1. **Bug**: Selected coordinates were inverted (x and y axes swapped).  
   **How Noticed**: The backend flagged incorrect coordinate mapping when processing guesses.  
   **Fix**: Adjusted coordinate conversion logic to correctly swap `x` and `y` before sending to the server.

2. **Bug**: Difficulty level changes did not immediately update UI elements.  
   **How Noticed**: After changing the difficulty, the remaining attempts text and other visuals didn't refresh.  
   **Fix**: Added logic to reload the page or dynamically update the DOM when the difficulty level changes.

3. **Bug**: Game crashed if no coordinates were selected before submitting.  
   **How Noticed**: Noticed during testing when accidentally clicking "Submit Guess" without prior map interaction.  
   **Fix**: Added validation to ensure coordinates are selected, and an alert prompts the user if no selection is made.

4. **Bug**: Incorrect attempts left after switching difficulty mid-game.  
   **How Noticed**: Observed that the remaining attempts weren't recalibrated correctly for the new difficulty.  
   **Fix**: Synced the difficulty changes with a reset mechanism for attempts.

5. **Bug**: SweetAlert popups caused page interactions to freeze in rare cases.  
   **How Noticed**: Occurred during rapid-click testing of submit and retry options.  
   **Fix**: Debounced button events to prevent duplicate calls and ensure proper alert behavior.

6. **Bug**: Islands were not detected properly because diagonal connections between cells were not considered.  
   **How Noticed**: During testing, small diagonally connected clusters of land cells were treated as separate islands instead of being grouped as one.  
   **Fix**: Updated the island detection algorithm to include diagonal neighbors in addition to horizontal and vertical ones. Retested the logic using maps with various patterns to ensure accuracy.

7. **Bug**: Scaling of map coordinates broke on non-standard screen resolutions or zoom levels.  
   **How Noticed**: During testing on smaller devices and browsers with zoom enabled, clicks on the map didn't match the displayed cells.  
   **Fix**: Updated the coordinate scaling formula to account for device pixel ratio and viewport scaling. Tested thoroughly on different resolutions and browsers.

8. **Bug**: Attempts-left counter displayed incorrectly after page reload.  
   **How Noticed**: After refreshing the page mid-game, the "attempts left" counter showed a default value instead of the actual remaining attempts.  
   **Fix**: Synced the front-end with backend state using API calls during initialization to fetch the correct game progress.

9. **Bug**: Visual glitches when the map image failed to load or was resized.  
   **How Noticed**: Occurred when network speed was slow, or the map dimensions were changed dynamically during difficulty selection.  
   **Fix**: Added fallback logic to load a placeholder image and adjusted image rendering to handle resizing without distortion.


10. **Bug**: Multiple difficulty selection requests sent simultaneously caused the game state to break.  
   **How Noticed**: Discovered during rapid testing when difficulty buttons were clicked repeatedly.  
   **Fix**: Disabled the difficulty buttons temporarily after selection and re-enabled them after the server responded, preventing concurrent requests.

---

## Ways to Test Other Contestants' Projects

1. **Functional Testing**  
   - Verify if coordinates clicked on the map translate correctly to the backend.
   - Check if the remaining attempts decrease after each guess.
   - Ensure difficulty changes update the game rules dynamically.
   - Validate that game state (e.g., win, lose, or in progress) updates appropriately based on guesses.

2. **Boundary Testing**  
   - Click on the very edges and corners of the map to see if coordinates are processed correctly.
   - Test with all possible difficulty levels to ensure correct behavior for each.
   - Submit guesses for islands at the smallest and largest possible height values.

3. **Stress Testing**  
   - Rapidly click the "Submit Guess" button multiple times to observe if the system handles duplicate inputs gracefully.
   - Change difficulty multiple times in quick succession to check for stability.
   - Test with a large number of concurrent users to simulate heavy server load.

4. **Negative Testing**  
   - Attempt to submit a guess without selecting coordinates.
   - Modify the client-side code to send invalid or out-of-range data (e.g., negative coordinates) and verify if the backend handles it securely.
   - Disconnect the network mid-game and attempt to continue gameplay, checking how the app handles errors.

5. **Usability Testing**  
   - Observe how first-time players interact with the interface.
   - Check if error messages and feedback are clear and actionable.
   - Test accessibility features, such as compatibility with screen readers or keyboard navigation.

6. **Performance Testing**  
   - Evaluate load times for large map sizes.
   - Measure responsiveness across devices (desktop, tablet, and mobile).
   - Test on low-performance devices or browsers to ensure adequate performance.

7. **Security Testing**  
   - Attempt to inject malicious data into input fields or API requests to test for vulnerabilities.
   - Test if sensitive data (like difficulty levels or map data) is securely stored and transmitted.

8. **Edge Case Testing**  
   - Simulate scenarios where all islands have the same average height to check how ties are resolved.
   - Test maps with no land (only water) or all land (no water) to verify edge-case behavior.

9. **Error Handling Testing**  
   - Simulate a server failure or timeout during gameplay and verify how gracefully the application recovers.
   - Manually corrupt the map data or user state and test how the app handles invalid inputs.

10. **Localization Testing**  
    - Test the app with different language settings, ensuring text fits UI elements and no content is clipped.
    - Verify if date/time formats and number formatting adhere to local standards.

11. **Scalability Testing**  
    - Gradually increase the map size or the number of islands to evaluate how the game scales in terms of performance and usability.
    - Test with varying levels of network latency to observe effects on responsiveness.

12. **Game Mechanics Testing**  
    - Experiment with intentionally wrong guesses to ensure feedback encourages retrying.
    - Test the game's hint system (if implemented) to confirm it provides meaningful guidance without giving away the answer.

13. **User Experience Feedback**  
    - Conduct surveys or interviews with testers to gather qualitative feedback on the enjoyment and clarity of the game.
    - Analyze if users understand the rules and goals without needing extensive instructions.

By applying a combination of these tests, you can uncover potential flaws and ensure a robust and engaging game experience!


## Improvements/Features with a Magic Wand

1. **Real-Time Multiplayer Mode**  
   - Allow multiple players to compete simultaneously on the same map, guessing islands in turns.

2. **Enhanced Visuals and Animations**  
   - Introduce dynamic waves and island discovery animations for a more immersive experience.

3. **Procedural Map Generation**  
   - Generate maps dynamically with varying difficulty, terrain types, and environmental conditions.

4. **AI-Powered Suggestions**  
   - Provide optional hints based on guess history and island characteristics.

5. **Global Leaderboard**  
   - Create a competitive environment by displaying the best players worldwide.

6. **Offline Mode**  
   - Enable players to enjoy the game without an internet connection by saving progress locally.

7. **Custom Map Sizes**  
   - Allow players to select or create maps of different dimensions (e.g., 50x50, 100x100).

8. **Island Selection Timer**  
   - Add a time limit for each guess, where players have a set amount of time (e.g., 30 seconds) to choose an island. This could increase the game's intensity.

9. **Arcade Mode**  
   - Introduce an arcade mode where players must find as many islands as possible within a specific time limit, with scores based on the number of correct guesses.

---

## Factors That Could Affect the Solution

1. **Map Size**  
   - **Impact**: Larger maps would require better scaling algorithms and potentially affect responsiveness.  
   - **Solution**: Optimize map rendering using technologies like canvas or WebGL for smooth performance.

2. **Number of Lives**  
   - **Impact**: Fewer lives increase the challenge, while more lives make the game easier. This balance could affect player engagement.  
   - **Solution**: Dynamically adjust difficulty parameters based on player skill or provide custom settings.

3. **Device Performance**  
   - **Impact**: Older devices might struggle with rendering large maps or animations.  
   - **Solution**: Introduce performance modes to reduce animation and simplify graphics.

4. **User Input Precision**  
   - **Impact**: Clicking on small map areas might be challenging, especially on mobile devices.  
   - **Solution**: Implement zoom and pan features for better precision.

5. **Server(Backend) Latency**  
   - **Impact**: Delays in processing guesses might frustrate players.  
   - **Solution**: Use caching and server-side optimization to reduce latency.

6. **Player Demographics**  
   - **Impact**: Casual players may find it too challenging, while competitive players may want more depth.  
   - **Solution**: Offer both casual and competitive modes with tailored experiences.

7. **Lack of Proper Testing for Rare Scenarios**  
   - **Problem**: Unusual configurations like single-cell islands or maps entirely made of water might not be handled well.  
   - **Impact**: Game logic could break or produce nonsensical results.  
   - **Mitigation**: Test edge cases extensively and implement fallback logic for unsupported scenarios.

8. **Excessive Backend Load**  
   - **Problem**: High user traffic or inefficient server-side processing could slow down responses or cause crashes.  
   - **Impact**: Players might experience delays or complete game outages.  
   - **Mitigation**: Optimize server-side code, use load balancing, and implement rate-limiting mechanisms.

9.  **Scaling Issues with Click Coordinates**
   - **Problem**: Misalignment between the resized map displayed on the UI and the original dimensions used by the backend could lead to incorrect guesses.  
   - **Impact**: Players might feel their inputs are ignored or misinterpreted.  
   - **Mitigation**: Use consistent scaling formulas and test extensively on various screen sizes and resolutions.

10. **Backend Timeout When Processing Larger Maps**  
   - **Problem**: When working with larger map sizes, the backend may experience timeouts during island detection due to the complexity of the algorithm.  
   - **Impact**: The game may experience delays, crashes, or unresponsive behavior.  
   - **Mitigation**: Refactor and optimize the island detection algorithm, implement memoization, and introduce server-side optimizations to handle large data efficiently.
---

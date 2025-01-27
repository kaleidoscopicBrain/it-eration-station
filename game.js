// Initial game state
let money = 100;
let tasksCompleted = 0;
let cooldownTime = 5000; // in milliseconds
let moneyPerTask = 50;
let cooldownActive = false;

// Elements
const moneyElement = document.getElementById("money");
const tasksCompletedElement = document.getElementById("tasks-completed");
const cooldownTimeElement = document.getElementById("cooldown-time");
const writeCodeButton = document.getElementById("write_code");
const upgradeMoneyButton = document.getElementById("upgrade-money");
const upgradeCooldownButton = document.getElementById("upgrade-cooldown");

// Function to update the game info
function updateGameInfo() {
    moneyElement.textContent = `Money: $${money}`;
    tasksCompletedElement.textContent = `Tasks Completed: ${tasksCompleted}`;
    cooldownTimeElement.textContent = `Cooldown Time: ${cooldownTime / 1000}s`;
}

// Function to handle the Write Code action with progress bar
writeCodeButton.addEventListener("click", function() {
    if (!cooldownActive) {
        // Disable the button and start the progress bar
        writeCodeButton.disabled = true;
        const progressBar = writeCodeButton.querySelector(".progress-bar");
        progressBar.style.width = "100%"; // Start progress bar animation

        // Simulate task completion
        setTimeout(function() {
            money += moneyPerTask; // Add money per task
            tasksCompleted += 1; // Increment tasks completed
            updateGameInfo();

            // Reset the button and progress bar after task completion
            writeCodeButton.disabled = false;
            progressBar.style.width = "0%"; // Reset progress bar
        }, cooldownTime);
    } else {
        alert("Please wait for the cooldown!");
    }
});

// Function to purchase the upgrade (Money per task)
upgradeMoneyButton.addEventListener("click", function() {
    if (money >= 100) {
        money -= 100;
        moneyPerTask += 10; // Increase money per task
        updateGameInfo();
        alert("Upgrade successful! You now earn more money per task.");
    } else {
        alert("Not enough money for this upgrade.");
    }
});

// Function to purchase the upgrade (Cooldown time)
upgradeCooldownButton.addEventListener("click", function() {
    if (money >= 200) {
        money -= 200;
        cooldownTime -= 2000; // Decrease cooldown time by 2 seconds
        updateGameInfo();
        alert("Cooldown upgrade successful! Your cooldown time is reduced.");
    } else {
        alert("Not enough money for this upgrade.");
    }
});

// Initial game info update
updateGameInfo();

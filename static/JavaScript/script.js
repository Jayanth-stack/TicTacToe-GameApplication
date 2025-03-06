document.addEventListener("DOMContentLoaded", () => {
    const cells = document.querySelectorAll(".cell");
    const message = document.getElementById("message");
    const resetBtn = document.getElementById("reset-btn");
    const scoreX = document.getElementById("score-x");
    const scoreO = document.getElementById("score-o");

    cells.forEach(cell => {
        cell.addEventListener("click", () => handleMove(cell));
    });

    resetBtn.addEventListener("click", resetGame);

    function handleMove(cell) {
        const position = cell.getAttribute("data-index");

        fetch("/move", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ position: parseInt(position) })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                message.textContent = data.error;
                return;
            }
            updateBoard(data.board);
            scoreX.textContent = data.scores.X;
            scoreO.textContent = data.scores.O;

            if (data.winner) {
                message.textContent = data.winner === "Draw" ? "It's a Draw!" : `${data.winner} Wins!`;
            } else {
                message.textContent = `Player ${data.current_player}'s Turn`;
            }
        })
        .catch(error => console.error("Error:", error));
    }

    function updateBoard(board) {
        cells.forEach((cell, index) => {
            cell.textContent = board[index];
        });
    }

    function resetGame() {
        fetch("/reset", {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            updateBoard(data.board);
            message.textContent = `Player ${data.current_player}'s Turn`;
            scoreX.textContent = data.scores.X;
            scoreO.textContent = data.scores.O;
        })
        .catch(error => console.error("Error:", error));
    }
});
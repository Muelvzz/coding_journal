function showSidebar(){
    const sidebar = document.querySelector(".sidebar")
    sidebar.style.display = "flex"
}

function hideSidebar(){
    const sidebar = document.querySelector(".sidebar")
    sidebar.style.display = "none"
}

function search(){
    const query = document.getElementById("search-box").value.toLowerCase();
    const cards = document.querySelectorAll("#journals .card");

    cards.forEach(card => {
    const titleElement = card.querySelector("h5");
    const title = titleElement ? titleElement.textContent.toLowerCase() : "";

    if (title.includes(query)) {
        card.style.display = "block";
    }
    else {
        card.style.display = "none"
    }
    });
}

const ctx = document.getElementById("lineChart");
const lineChart = new Chart(ctx, {
    type: "line",
    data: {
        labels: dateEntries,
        datasets: [{
            label: "Journals",
            data: journalAnalysis,
            fill: false,
            borderColor: "rgb(75, 192, 192)",
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});

const passwordInput = document.getElementById('password');
const togglePasswordButton = document.getElementById('togglePassword');

togglePasswordButton.addEventListener('click', () => {
  const type = passwordInput.type === 'password' ? 'text' : 'password';
  passwordInput.type = type;

  // Change button text
  togglePasswordButton.textContent = type === 'password' ? 'Show' : 'Hide';
});
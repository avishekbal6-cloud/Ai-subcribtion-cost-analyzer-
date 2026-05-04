const API = "http://127.0.0.1:5000";

let chart;

// ================= NAVIGATION =================
function showSection(id) {
    document.querySelectorAll(".section").forEach(sec => {
        sec.classList.add("hidden");
    });

    document.getElementById(id).classList.remove("hidden");

    document.querySelectorAll(".sidebar a").forEach(a => {
        a.classList.remove("active");
    });

    event.target.classList.add("active");
}

// ================= DASHBOARD =================
async function loadDashboard() {
    const rev = await fetch(`${API}/revenue`).then(r => r.json());
    document.getElementById("revenue").innerText = "₹ " + rev.total_revenue;

    const churn = await fetch(`${API}/churn`).then(r => r.json());
    document.getElementById("churn").innerText = churn.churn_rate + "%";

    const watch = await fetch(`${API}/watch-time`).then(r => r.json());
    document.getElementById("watch").innerText = watch.average_watch_time + " mins";
}

// ================= CHART =================
async function loadChart() {
    const data = await fetch(`${API}/revenue-by-plan`).then(r => r.json());

    if (chart) chart.destroy();

    const ctx = document.getElementById("chart").getContext("2d");

    chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: "Revenue",
                data: Object.values(data),
                backgroundColor: ["#00c6ff", "#0072ff", "#00ffae"]
            }]
        }
    });
}

// ================= PREDICTION =================
async function predictChurn() {
    const res = await fetch(`${API}/predict`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            age: document.getElementById("age").value,
            country: document.getElementById("country").value,
            subscription: document.getElementById("subscription").value,
            monthly_fee: document.getElementById("fee").value,
            watch_time: document.getElementById("watch_time").value
        })
    });

    const data = await res.json();

    document.getElementById("result").innerText =
        `Churn: ${data.churn} (Confidence: ${data.confidence}%)`;
}

// INIT
loadDashboard();
loadChart();
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
import os

# HTML content (your provided HTML code)
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bandhu - JEE Study Tracker</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
            min-height: 100vh;
            color: #1f2937;
            line-height: 1.6;
            font-size: 1.1rem;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        h1 {
            font-size: 2rem;
            font-weight: 800;
            color: #1f2937;
            margin-bottom: 2rem;
            text-align: center;
        }

        .tabs {
            display: flex;
            border-bottom: 2px solid #d1d5db;
            margin-bottom: 2rem;
        }

        .tab-button {
            padding: 1rem 2rem;
            background-color: #f3f4f6;
            color: #1f2937;
            font-weight: 600;
            font-size: 1.1rem;
            border: none;
            border-radius: 0.5rem 0.5rem 0 0;
            cursor: pointer;
            margin-right: 0.5rem;
            transition: all 0.3s ease;
        }

        .tab-button:hover {
            background-color: #d1d5db;
        }

        .tab-button.active {
            background-color: #4f46e5;
            color: white;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .card {
            background-color: white;
            border: 1px solid #e5e7eb;
            border-radius: 0.5rem;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .card h3 {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
        }

        .quote-section {
            background: linear-gradient(to right, #4f46e5, #7c3aed);
            color: white;
            border-radius: 0.5rem;
            padding: 2rem;
        }

        .quote-section p {
            font-size: 1.25rem;
            font-style: italic;
            margin-bottom: 1.5rem;
        }

        .streak-section {
            margin-top: 1.5rem;
            font-size: 1.1rem;
            font-weight: 600;
        }

        .button {
            background-color: #4f46e5;
            color: white;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 0.375rem;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .button:hover {
            background-color: #6d28d9;
        }

        .progress-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
            gap: 2rem;
        }

        .progress-item {
            display: flex;
            flex-direction: column;
        }

        .progress-item h4 {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }

        .progress-bar {
            background-color: #e5e7eb;
            border-radius: 0.375rem;
            overflow: hidden;
            height: 1.75rem;
            position: relative;
        }

        .progress-bar-fill {
            height: 100%;
            transition: width 0.5s ease-in-out;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 0.5rem;
            color: white;
            font-size: 0.9rem;
            font-weight: 600;
        }

        .progress-bar-fill.physics { background-color: #ef4444; }
        .progress-bar-fill.chemistry { background-color: #10b981; }
        .progress-bar-fill.mathematics { background-color: #3b82f6; }

        .chart-container {
            width: 100%;
            max-height: 26rem;
            margin-bottom: 2rem;
        }

        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .stats-item {
            background-color: #f9fafb;
            padding: 1rem;
            border-radius: 0.375rem;
            text-align: center;
        }

        .stats-item h4 {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .stats-item p {
            font-size: 1.25rem;
            font-weight: 700;
            color: #4f46e5;
        }

        .entry-form, .goal-form {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr));
            gap: 2rem;
        }

        .form-group {
            display: flex;
            flex-direction: column;
        }

        .form-group label {
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 0.75rem;
        }

        .input-group {
            display: flex;
            align-items: center;
        }

        .input-group input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #d1d5db;
            border-radius: 0.375rem 0 0 0.375rem;
            font-size: 1rem;
            text-align: center;
            border-right: none;
        }

        .input-group input:focus {
            outline: none;
            border-color: #4f46e5;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
        }

        .input-group button {
            padding: 0.75rem 1rem;
            border: 1px solid #d1d5db;
            background-color: #f3f4f6;
            color: #1f2937;
            font-size: 1rem;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .input-group button:hover {
            background-color: #d1d5db;
        }

        .input-group button:first-of-type {
            border-radius: 0 0.375rem 0.375rem 0;
            border-left: none;
        }

        .goal-form input {
            padding: 0.75rem;
            border: 1px solid #d1d5db;
            border-radius: 0.375rem;
            font-size: 1rem;
            transition: all 0.2s ease;
        }

        .goal-form input:focus {
            outline: none;
            border-color: #4f46e5;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
        }

        .date-display {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            color: #4b5563;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 1.1rem;
            max-height: 20rem;
            display: block;
            overflow-y: auto;
        }

        th, td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
            min-width: 7rem;
        }

        th {
            background-color: #f3f4f6;
            font-weight: 700;
            position: sticky;
            top: 0;
            z-index: 1;
        }

        tr:hover {
            background-color: #f9fafb;
        }

        .action-button {
            padding: 0.5rem 1.25rem;
            margin: 0 0.5rem;
            font-size: 0.9rem;
            cursor: pointer;
            background-color: #4f46e5;
            color: white;
            border: none;
            border-radius: 0.375rem;
            transition: background-color 0.3s ease;
        }

        .action-button:hover {
            background-color: #6d28d9;
        }

        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }

            .tabs {
                flex-direction: column;
            }

            .tab-button {
                width: 100%;
                margin-right: 0;
                margin-bottom: 0.5rem;
                border-radius: 0.375rem;
            }

            .progress-container, .stats-container {
                grid-template-columns: 1fr;
            }

            .entry-form, .goal-form {
                grid-template-columns: 1fr;
            }

            table {
                font-size: 0.95rem;
            }

            th, td {
                padding: 0.5rem;
                min-width: 5rem;
            }

            .action-button {
                padding: 0.4rem 0.8rem;
                font-size: 0.8rem;
            }

            .input-group button {
                padding: 0.5rem 0.75rem;
                font-size: 0.9rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Bandhu - JEE Study Tracker</h1>
        <div class="tabs">
            <button id="dashboard-tab" class="tab-button active">Dashboard</button>
            <button id="entry-tab" class="tab-button">Entry</button>
            <button id="goals-tab" class="tab-button">Goals</button>
            <button id="history-tab" class="tab-button">History</button>
        </div>

        <!-- Dashboard Tab -->
        <div id="dashboard" class="tab-content active">
            <div class="card quote-section">
                <h3>Welcome</h3>
                <p id="quote"></p>
                <div class="streak-section">
                    <span>Current Streak: <span id="streak">0</span> days</span>
                </div>
                <button id="new-quote" class="button">New Quote</button>
            </div>
            <div class="card">
                <h3>Today's Progress (Questions Solved)</h3>
                <div class="progress-container">
                    <div class="progress-item">
                        <h4 style="color: #ef4444;">Physics</h4>
                        <div class="progress-bar">
                            <div id="physics-progress" class="progress-bar-fill physics">0/0</div>
                        </div>
                    </div>
                    <div class="progress-item">
                        <h4 style="color: #10b981;">Chemistry</h4>
                        <div class="progress-bar">
                            <div id="chemistry-progress" class="progress-bar-fill chemistry">0/0</div>
                        </div>
                    </div>
                    <div class="progress-item">
                        <h4 style="color: #3b82f6;">Mathematics</h4>
                        <div class="progress-bar">
                            <div id="mathematics-progress" class="progress-bar-fill mathematics">0/0</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card">
                <h3>Study Analysis</h3>
                <div class="stats-container">
                    <div class="stats-item">
                        <h4>Average Questions/Day</h4>
                        <p id="avg-questions">0</p>
                    </div>
                    <div class="stats-item">
                        <h4>Total Questions</h4>
                        <p id="total-questions">0</p>
                    </div>
                    <div class="stats-item">
                        <h4>Goal Completion</h4>
                        <p id="goal-completion">0%</p>
                    </div>
                </div>
                <div class="chart-container">
                    <h4>Daily Progress (Last 7 Days)</h4>
                    <canvas id="lineChart"></canvas>
                </div>
                <div class="chart-container">
                    <h4>Total Questions per Day</h4>
                    <canvas id="barChart"></canvas>
                </div>
                <div class="chart-container">
                    <h4>Subject Distribution (This Week)</h4>
                    <canvas id="pieChart"></canvas>
                </div>
                <div class="chart-container">
                    <h4>Subject-Wise Daily Progress</h4>
                    <canvas id="stackedBarChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Entry Tab -->
        <div id="entry" class="tab-content">
            <div class="card">
                <h3>Daily Entry (Questions Solved)</h3>
                <div class="date-display" id="current-date">Editing for: YYYY-MM-DD</div>
                <div class="entry-form">
                    <div class="form-group">
                        <label style="color: #ef4444;">Physics</label>
                        <div class="input-group">
                            <input id="physics-input" type="number" min="0" step="1" value="0">
                            <button onclick="increment('physics')">+</button>
                            <button onclick="decrement('physics')">-</button>
                        </div>
                    </div>
                    <div class="form-group">
                        <label style="color: #10b981;">Chemistry</label>
                        <div class="input-group">
                            <input id="chemistry-input" type="number" min="0" step="1" value="0">
                            <button onclick="increment('chemistry')">+</button>
                            <button onclick="decrement('chemistry')">-</button>
                        </div>
                    </div>
                    <div class="form-group">
                        <label style="color: #3b82f6;">Mathematics</label>
                        <div class="input-group">
                            <input id="mathematics-input" type="number" min="0" step="1" value="0">
                            <button onclick="increment('mathematics')">+</button>
                            <button onclick="decrement('mathematics')">-</button>
                        </div>
                    </div>
                </div>
                <button id="save-entry" class="button" style="margin-top: 1.5rem;">Save Entry</button>
            </div>
        </div>

        <!-- Goals Tab -->
        <div id="goals" class="tab-content">
            <div class="card">
                <h3>Set Daily Goals (Questions)</h3>
                <div class="goal-form">
                    <div class="form-group">
                        <label style="color: #ef4444;">Physics</label>
                        <input id="physics-goal" type="number" min="0" step="1" value="10">
                    </div>
                    <div class="form-group">
                        <label style="color: #10b981;">Chemistry</label>
                        <input id="chemistry-goal" type="number" min="0" step="1" value="10">
                    </div>
                    <div class="form-group">
                        <label style="color: #3b82f6;">Mathematics</label>
                        <input id="mathematics-goal" type="number" min="0" step="1" value="10">
                    </div>
                </div>
                <button id="save-goals" class="button" style="margin-top: 1.5rem;">Save Goals</button>
            </div>
            <div class="card">
                <h3>Data Management</h3>
                <button id="export-data" class="button">Export Data</button>
                <button id="import-data" class="button" style="margin-left: 0.75rem;">Import Data</button>
            </div>
        </div>

        <!-- History Tab -->
        <div id="history" class="tab-content">
            <div class="card">
                <h3>Study History</h3>
                <div style="overflow-x: auto; max-height: 20rem;">
                    <table id="history-table">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Physics</th>
                                <th>Chemistry</th>
                                <th>Mathematics</th>
                                <th>Total</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="history-table-body"></tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
        const colors = {
            physics: '#ef4444',
            chemistry: '#10b981',
            mathematics: '#3b82f6'
        };

        const subjects = ['physics', 'chemistry', 'mathematics'];
        const quotes = [
            "Success is small efforts repeated daily!",
            "Every problem solved makes you stronger!",
            "Consistency beats perfection!",
            "Stay focused, stay determined!",
            "Every step forward counts!",
            "Hard work beats talent when talent doesn't work hard!",
            "Keep pushing, you're closer than you think!",
            "Dream big, work hard, stay focused!",
            "The journey of a thousand miles begins with a single step!",
            "Your only limit is your mind!"
        ];

        // Data Management
        function loadData() {
            const defaultData = {
                history: {},
                goals: { physics: 10, chemistry: 10, mathematics: 10 },
                streak: { count: 0, lastDate: null }
            };
            const currentDate = new Date().toISOString().split('T')[0];
            defaultData.history[currentDate] = { physics: 0, chemistry: 0, mathematics: 0 };

            const savedData = localStorage.getItem('studyData');
            if (savedData) {
                try {
                    const data = JSON.parse(savedData);
                    data.history = data.history || {};
                    data.goals = data.goals || { physics: 10, chemistry: 10, mathematics: 10 };
                    data.streak = data.streak || { count: 0, lastDate: null };
                    if (!data.history[currentDate]) {
                        data.history[currentDate] = { physics: 0, chemistry: 0, mathematics: 0 };
                    }
                    return data;
                } catch (err) {
                    alert('Failed to load saved data. Using default data.');
                }
            }
            localStorage.setItem('studyData', JSON.stringify(defaultData));
            return defaultData;
        }

        function saveData(data) {
            try {
                localStorage.setItem('studyData', JSON.stringify(data));
            } catch (err) {
                alert('Failed to save data to local storage.');
            }
        }

        // Streak Calculation
        function calculateStreak(history) {
            const dates = Object.keys(history).sort((a, b) => new Date(b) - new Date(a));
            let streak = 0;
            let current = new Date();
            let expectedDate = current.toISOString().split('T')[0];

            for (let date of dates) {
                if (date === expectedDate && Object.values(history[date]).some(val => val > 0)) {
                    streak++;
                    current.setDate(current.getDate() - 1);
                    expectedDate = current.toISOString().split('T')[0];
                } else {
                    break;
                }
            }
            return streak;
        }

        // Analysis Calculations
        function calculateStats(data) {
            const history = data.history;
            const dates = Object.keys(history);
            const totals = { physics: 0, chemistry: 0, mathematics: 0, total: 0 };
            let daysWithData = 0;
            let goalsMet = 0;

            dates.forEach(date => {
                const entry = history[date];
                const dayTotal = (entry.physics || 0) + (entry.chemistry || 0) + (entry.mathematics || 0);
                if (dayTotal > 0) {
                    daysWithData++;
                    totals.physics += entry.physics || 0;
                    totals.chemistry += entry.chemistry || 0;
                    totals.mathematics += entry.mathematics || 0;
                    totals.total += dayTotal;
                    const goals = data.goals;
                    if ((entry.physics || 0) >= (goals.physics || 10) &&
                        (entry.chemistry || 0) >= (goals.chemistry || 10) &&
                        (entry.mathematics || 0) >= (goals.mathematics || 10)) {
                        goalsMet++;
                    }
                }
            });

            const avgQuestions = daysWithData > 0 ? (totals.total / daysWithData).toFixed(1) : 0;
            const goalCompletion = daysWithData > 0 ? ((goalsMet / daysWithData) * 100).toFixed(1) : 0;

            return {
                avgQuestions,
                totalQuestions: totals.total,
                goalCompletion,
                subjectTotals: totals
            };
        }

        // UI Updates
        function updateQuote() {
            document.getElementById('quote').textContent = quotes[Math.floor(Math.random() * quotes.length)];
        }

        function updateProgressBars(data, currentDate) {
            subjects.forEach(subject => {
                const value = data.history[currentDate]?.[subject] || 0;
                const max = data.goals[subject] || 1;
                const percentage = Math.min((value / max) * 100, 100);
                const progressBar = document.getElementById(`${subject}-progress`);
                progressBar.style.width = `${percentage}%`;
                progressBar.textContent = `${value} / ${max}`;
            });
        }

        function updateCharts(data, currentDate) {
            const last7Days = Array.from({ length: 7 }, (_, i) => {
                const d = new Date();
                d.setDate(d.getDate() - i);
                return d.toISOString().split('T')[0];
            }).reverse();

            // Line Chart
            const lineCtx = document.getElementById('lineChart');
            if (lineCtx && window.Chart) {
                try {
                    if (window.lineChart && typeof window.lineChart.destroy === 'function') {
                        window.lineChart.destroy();
                    }
                    window.lineChart = new Chart(lineCtx.getContext('2d'), {
                        type: 'line',
                        data: {
                            labels: last7Days.map(d => new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })),
                            datasets: subjects.map(subject => ({
                                label: subject.charAt(0).toUpperCase() + subject.slice(1),
                                data: last7Days.map(date => data.history[date]?.[subject] || 0),
                                borderColor: colors[subject],
                                fill: false,
                                tension: 0.4
                            }))
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: { beginAtZero: true, title: { display: true, text: 'Questions Solved' } },
                                x: { title: { display: true, text: 'Date' } }
                            },
                            plugins: {
                                legend: { position: 'top' },
                                title: { display: true, text: 'Daily Progress (Last 7 Days)', font: { size: 16 } }
                            }
                        }
                    });
                } catch (err) {
                    console.error('Line chart initialization error:', err);
                }
            }

            // Bar Chart (Total Questions per Day)
            const barCtx = document.getElementById('barChart');
            if (barCtx && window.Chart) {
                try {
                    if (window.barChart && typeof window.barChart.destroy === 'function') {
                        window.barChart.destroy();
                    }
                    window.barChart = new Chart(barCtx.getContext('2d'), {
                        type: 'bar',
                        data: {
                            labels: last7Days.map(d => new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })),
                            datasets: [{
                                label: 'Total Questions',
                                data: last7Days.map(date => {
                                    const entry = data.history[date] || { physics: 0, chemistry: 0, mathematics: 0 };
                                    return (entry.physics || 0) + (entry.chemistry || 0) + (entry.mathematics || 0);
                                }),
                                backgroundColor: '#4f46e5'
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: { beginAtZero: true, title: { display: true, text: 'Total Questions' } },
                                x: { title: { display: true, text: 'Date' } }
                            },
                            plugins: {
                                legend: { display: false },
                                title: { display: true, text: 'Total Questions per Day', font: { size: 16 } }
                            }
                        }
                    });
                } catch (err) {
                    console.error('Bar chart initialization error:', err);
                }
            }

            // Pie Chart (Subject Distribution)
            const pieCtx = document.getElementById('pieChart');
            if (pieCtx && window.Chart) {
                try {
                    if (window.pieChart && typeof window.pieChart.destroy === 'function') {
                        window.pieChart.destroy();
                    }
                    const totals = calculateStats(data).subjectTotals;
                    window.pieChart = new Chart(pieCtx.getContext('2d'), {
                        type: 'pie',
                        data: {
                            labels: subjects.map(s => s.charAt(0).toUpperCase() + s.slice(1)),
                            datasets: [{
                                data: subjects.map(subject => totals[subject] || 0),
                                backgroundColor: subjects.map(subject => colors[subject])
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: { position: 'right' },
                                title: { display: true, text: 'Subject Distribution', font: { size: 16 } }
                            }
                        }
                    });
                } catch (err) {
                    console.error('Pie chart initialization error:', err);
                }
            }

            // Stacked Bar Chart
            const stackedBarCtx = document.getElementById('stackedBarChart');
            if (stackedBarCtx && window.Chart) {
                try {
                    if (window.stackedBarChart && typeof window.stackedBarChart.destroy === 'function') {
                        window.stackedBarChart.destroy();
                    }
                    window.stackedBarChart = new Chart(stackedBarCtx.getContext('2d'), {
                        type: 'bar',
                        data: {
                            labels: last7Days.map(d => new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })),
                            datasets: subjects.map(subject => ({
                                label: subject.charAt(0).toUpperCase() + subject.slice(1),
                                data: last7Days.map(date => data.history[date]?.[subject] || 0),
                                backgroundColor: colors[subject]
                            }))
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: { beginAtZero: true, title: { display: true, text: 'Questions Solved' }, stacked: true },
                                x: { title: { display: true, text: 'Date' }, stacked: true }
                            },
                            plugins: {
                                legend: { position: 'top' },
                                title: { display: true, text: 'Subject-Wise Daily Progress', font: { size: 16 } }
                            }
                        }
                    });
                } catch (err) {
                    console.error('Stacked bar chart initialization error:', err);
                }
            }
        }

        function updateStats(data) {
            const stats = calculateStats(data);
            document.getElementById('avg-questions').textContent = stats.avgQuestions;
            document.getElementById('total-questions').textContent = stats.totalQuestions;
            document.getElementById('goal-completion').textContent = `${stats.goalCompletion}%`;
        }

        function updateHistoryTable(data) {
            const tbody = document.getElementById('history-table-body');
            tbody.innerHTML = '';
            const historyEntries = Object.keys(data.history).sort((a, b) => new Date(b) - new Date(a));
            historyEntries.forEach(date => {
                const row = document.createElement('tr');
                const total = (data.history[date].physics || 0) + (data.history[date].chemistry || 0) + (data.history[date].mathematics || 0);
                row.innerHTML = `
                    <td>${date}</td>
                    <td>${data.history[date].physics || 0}</td>
                    <td>${data.history[date].chemistry || 0}</td>
                    <td>${data.history[date].mathematics || 0}</td>
                    <td>${total}</td>
                    <td>
                        <button class="action-button" onclick="editEntry('${date}')">Edit</button>
                        <button class="action-button" onclick="deleteEntry('${date}')">Delete</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }

        function updateStreak(data) {
            const streak = calculateStreak(data.history);
            document.getElementById('streak').textContent = streak;
        }

        function updateEntryInputs(data, currentDate) {
            subjects.forEach(subject => {
                const input = document.getElementById(`${subject}-input`);
                input.value = data.history[currentDate]?.[subject] || 0;
            });
            document.getElementById('current-date').textContent = `Editing for: ${currentDate}`;
        }

        function updateAllDisplays(data, currentDate) {
            updateProgressBars(data, currentDate);
            updateCharts(data, currentDate);
            updateStats(data);
            updateHistoryTable(data);
            updateStreak(data);
            updateEntryInputs(data, currentDate);
        }

        // Tab Management
        function setActiveTab(tabId) {
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            document.getElementById(`${tabId}-tab`).classList.add('active');
            document.getElementById(tabId).classList.add('active');
            if (tabId === 'entry') {
                updateEntryInputs(data, currentDate);
            }
        }

        // Input Increment/Decrement
        function increment(subject) {
            const input = document.getElementById(`${subject}-input`);
            let value = parseInt(input.value) || 0;
            input.value = value + 1;
        }

        function decrement(subject) {
            const input = document.getElementById(`${subject}-input`);
            let value = parseInt(input.value) || 0;
            if (value > 0) {
                input.value = value - 1;
            }
        }

        // Input Validation
        function validateInputs() {
            subjects.forEach(subject => {
                ['input', 'goal'].forEach(type => {
                    const input = document.getElementById(`${subject}-${type}`);
                    input.addEventListener('input', () => {
                        let value = parseInt(input.value);
                        if (isNaN(value) || value < 0) {
                            input.value = 0;
                            alert(`Value for ${subject.charAt(0).toUpperCase() + subject.slice(1)} cannot be negative.`);
                        }
                    });
                });
            });
        }

        // Edit and Delete Entries
        function editEntry(date) {
            const entry = data.history[date];
            if (!entry) return;
            subjects.forEach(subject => {
                document.getElementById(`${subject}-input`).value = entry[subject] || 0;
            });
            currentDate = date; // Temporarily set currentDate to the edited date
            setActiveTab('entry');
            document.getElementById('current-date').textContent = `Editing for: ${date}`;
            const saveButton = document.getElementById('save-entry');
            saveButton.textContent = 'Update Entry';
            saveButton.onclick = () => {
                const newData = JSON.parse(JSON.stringify(data));
                subjects.forEach(subject => {
                    const value = parseInt(document.getElementById(`${subject}-input`).value) || 0;
                    newData.history[currentDate][subject] = value;
                });
                data = newData;
                saveData(data);
                updateAllDisplays(data, currentDate);
                saveButton.textContent = 'Save Entry';
                saveButton.onclick = saveEntryHandler;
                currentDate = new Date().toISOString().split('T')[0]; // Reset to today
                updateEntryInputs(data, currentDate);
                alert('Entry updated successfully!');
            };
        }

        function deleteEntry(date) {
            if (confirm(`Delete entry for ${date}?`)) {
                const newData = JSON.parse(JSON.stringify(data));
                delete newData.history[date];
                data = newData;
                saveData(data);
                updateAllDisplays(data, currentDate);
                alert('Entry deleted successfully!');
            }
        }

        // Data Export/Import
        function exportData(data) {
            try {
                const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'jee_study_data.json';
                a.click();
                URL.revokeObjectURL(url);
                alert('Data exported successfully!');
            } catch (err) {
                alert('Failed to export data.');
            }
        }

        function importData() {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.json';
            input.onchange = async (e) => {
                const file = e.target.files[0];
                if (file) {
                    try {
                        const text = await file.text();
                        const importedData = JSON.parse(text);
                        if (!importedData.history || !importedData.goals) {
                            alert('Invalid data format!');
                            return;
                        }
                        data = {
                            history: importedData.history || {},
                            goals: importedData.goals || { physics: 10, chemistry: 10, mathematics: 10 },
                            streak: importedData.streak || { count: 0, lastDate: null }
                        };
                        if (!data.history[currentDate]) {
                            data.history[currentDate] = { physics: 0, chemistry: 0, mathematics: 0 };
                        }
                        saveData(data);
                        updateAllDisplays(data, currentDate);
                        alert('Data imported successfully!');
                    } catch (err) {
                        alert('Invalid or corrupted JSON file!');
                    }
                }
            };
            input.click();
        }

        // Initialization
        let data = loadData();
        let currentDate = new Date().toISOString().split('T')[0];

        // Check if Chart.js is loaded
        if (!window.Chart) {
            alert('Chart.js failed to load. Some features may be unavailable.');
        }

        updateQuote();
        validateInputs();
        updateAllDisplays(data, currentDate);

        // Event Listeners
        document.getElementById('new-quote').addEventListener('click', updateQuote);

        const saveEntryHandler = () => {
            const newData = JSON.parse(JSON.stringify(data));
            subjects.forEach(subject => {
                const value = parseInt(document.getElementById(`${subject}-input`).value) || 0;
                if (value < 0) {
                    alert(`Value for ${subject.charAt(0).toUpperCase() + subject.slice(1)} cannot be negative.`);
                    return;
                }
                newData.history[currentDate][subject] = value;
            });
            data = newData;
            saveData(data);
            updateAllDisplays(data, currentDate);
            alert('Entry saved successfully!');
        };
        document.getElementById('save-entry').addEventListener('click', saveEntryHandler);

        document.getElementById('save-goals').addEventListener('click', () => {
            const newData = JSON.parse(JSON.stringify(data));
            subjects.forEach(subject => {
                const value = parseInt(document.getElementById(`${subject}-goal`).value) || 10;
                if (value < 0) {
                    alert(`Goal for ${subject.charAt(0).toUpperCase() + subject.slice(1)} cannot be negative.`);
                    return;
                }
                newData.goals[subject] = value;
            });
            data = newData;
            saveData(data);
            updateAllDisplays(data, currentDate);
            alert('Goals saved successfully!');
        });

        document.getElementById('export-data').addEventListener('click', () => exportData(data));
        document.getElementById('import-data').addEventListener('click', importData);

        document.getElementById('dashboard-tab').addEventListener('click', () => setActiveTab('dashboard'));
        document.getElementById('entry-tab').addEventListener('click', () => setActiveTab('entry'));
        document.getElementById('goals-tab').addEventListener('click', () => setActiveTab('goals'));
        document.getElementById('history-tab').addEventListener('click', () => setActiveTab('history'));

        // Date Change Check
        setInterval(() => {
            const today = new Date().toISOString().split('T')[0];
            if (today !== currentDate) {
                currentDate = today;
                data.history[currentDate] = { physics: 0, chemistry: 0, mathematics: 0 };
                saveData(data);
                updateAllDisplays(data, currentDate);
            }
        }, 300000); // Check every 5 minutes
    </script>
</body>
</html>
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bandhu - JEE Study Tracker")
        self.setGeometry(100, 100, 1280, 720)  # Set window size

        # Create QWebEngineView to render HTML
        self.web_view = QWebEngineView(self)
        self.setCentralWidget(self.web_view)

        # Write HTML content to a temporary file
        self.html_file = "index.html"
        with open(self.html_file, "w", encoding="utf-8") as f:
            f.write(HTML_CONTENT)

        # Load the HTML file
        self.web_view.setUrl(QUrl.fromLocalFile(os.path.abspath(self.html_file)))

    def closeEvent(self, event):
        # Clean up the temporary HTML file when closing
        if os.path.exists(self.html_file):
            try:
                os.remove(self.html_file)
            except Exception:
                pass
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

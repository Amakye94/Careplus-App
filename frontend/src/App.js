import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header>
        <h1>Care+ Amakye @</h1>
        <button id="addPatientBtn" className="button">+ New Patient</button>
      </header>

      <main>
        {/* Summary Section */}
        <section className="summary">
          <div className="summary-card">
            <h2 id="totalPatients">0</h2>
            <p>Total Patients</p>
          </div>
          <div className="summary-card">
            <h2 id="avgGlucose">–</h2>
            <p>Average Glucose (mg/dL)</p>
          </div>
          <div className="summary-card">
            <h2 id="totalAlerts">0</h2>
            <p>Alerts</p>
          </div>
        </section>

        {/* Search bar */}
        <section className="search-bar">
          <input id="searchInput" type="text" placeholder="Search patient by name..." />
        </section>

        {/* Patient list */}
        <section id="patients" className="cards"></section>

        {/* System chart */}
        <section className="card">
          <h3>System Glucose Trend (All Patients)</h3>
          <canvas id="systemChart" height="100"></canvas>
        </section>
      </main>
    </div>
  );
}

export default App;

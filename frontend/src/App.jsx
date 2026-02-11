import React, { useState } from "react";
import Chart from "react-apexcharts";
import "./App.css";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("carScopeToken"));
  const [isLoginView, setIsLoginView] = useState(true);
  const [authData, setAuthData] = useState({
    username: "",
    email: "",
    password: "",
  });
  const [formData, setFormData] = useState({
    brand: "",
    model: "",
    fuel_type: "petrol",
    year: 2022,
    km_per_year: 15000,
    fuel_consumption: 6.5,
    engine_capacity: 1600,
    driver_age: 30,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // --- AUTENTIFICARE ---
  const handleAuth = async (e) => {
    e.preventDefault();
    setLoading(true);
    const endpoint = isLoginView ? "/login" : "/register";

    try {
      const response = await fetch(`http://127.0.0.1:8000${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: authData.username.trim(),
          email: authData.email.trim(),
          password: authData.password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        if (isLoginView) {
          localStorage.setItem("carScopeToken", data.access_token);
          setToken(data.access_token);
        } else {
          alert("Cont creat! Acum te poți loga.");
          setIsLoginView(true);
        }
      } else {
        alert(
          "Eroare: " +
            (data.detail?.[0]?.msg || data.detail || "Date invalide"),
        );
      }
    } catch (err) {
      alert("Serverul nu răspunde!");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("carScopeToken");
    setToken(null);
    setResult(null);
  };

  // --- CALCUL ---
  const handleCalculate = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          ...formData,
          year: parseInt(formData.year),
          km_per_year: parseInt(formData.km_per_year),
          fuel_consumption: parseFloat(formData.fuel_consumption),
          engine_capacity: parseInt(formData.engine_capacity),
          driver_age: parseInt(formData.driver_age),
        }),
      });

      const data = await response.json();
      if (response.ok) setResult(data);
      else alert("Sesiune expirată sau date invalide!");
    } catch (err) {
      alert("Eroare la calcul!");
    } finally {
      setLoading(false);
    }
  };

  // --- CONFIG GRAFICE ---
  const areaOptions = {
    chart: { toolbar: { show: false }, background: "transparent" },
    colors: ["#38bdf8"],
    theme: { mode: "dark" },
    stroke: { curve: "smooth" },
    xaxis: {
      categories: ["An 1", "An 2", "An 3", "An 4", "An 5"],
      labels: { style: { colors: "#94a3b8" } },
    },
    yaxis: {
      labels: {
        formatter: (val) => val.toFixed(0),
        style: { colors: "#94a3b8" },
      },
    },
    dataLabels: { enabled: true, formatter: (val) => val.toFixed(2) },
  };

  const donutOptions = {
    labels: ["Combustibil", "Asigurare", "Mentenanță"],
    colors: ["#38bdf8", "#818cf8", "#c084fc"],
    theme: { mode: "dark" },
    legend: { position: "bottom" },
    plotOptions: {
      donut: {
        size: "65%",
        labels: {
          show: true,
          total: {
            show: true,
            label: "TOTAL",
            formatter: () => result?.total.monthly.toFixed(0),
          },
        },
      },
    },
  };

  if (!token) {
    return (
      <div className="login-container">
        <header className="app-header">
          <h1>CarScope</h1>
          <p>Smart auto budget tracker</p>
        </header>
        <div className="card login-card">
          <h2>{isLoginView ? "Autentificare" : "Creează Cont"}</h2>
          <form
            onSubmit={handleAuth}
            style={{ display: "flex", flexDirection: "column", gap: "15px" }}
          >
            <input
              placeholder="Utilizator"
              onChange={(e) =>
                setAuthData({ ...authData, username: e.target.value })
              }
              required
            />
            <input
              type="email"
              placeholder="Email"
              onChange={(e) =>
                setAuthData({ ...authData, email: e.target.value })
              }
              required
            />
            <input
              type="password"
              placeholder="Parolă"
              onChange={(e) =>
                setAuthData({ ...authData, password: e.target.value })
              }
              required
            />
            <button type="submit" disabled={loading}>
              {loading
                ? "Așteaptă..."
                : isLoginView
                  ? "LOGARE"
                  : "ÎNREGISTRARE"}
            </button>
          </form>
          <button
            className="auth-toggle"
            onClick={() => setIsLoginView(!isLoginView)}
          >
            {isLoginView
              ? "Nu ai cont? Înregistrează-te"
              : "Ai deja cont? Loghează-te"}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="nav-header">
        <h1>CarScope</h1>
        <button onClick={handleLogout} className="logout-btn">
          Ieșire
        </button>
      </div>

      {!result ? (
        <div className="card">
          <form onSubmit={handleCalculate} className="smart-form">
            <div className="input-group">
              <label>MARCĂ</label>
              <input
                name="brand"
                placeholder="BMW"
                onChange={(e) =>
                  setFormData({ ...formData, brand: e.target.value })
                }
                required
              />
            </div>
            <div className="input-group">
              <label>MODEL</label>
              <input
                name="model"
                placeholder="Seria 3"
                onChange={(e) =>
                  setFormData({ ...formData, model: e.target.value })
                }
                required
              />
            </div>
            <div className="input-group">
              <label>COMBUSTIBIL</label>
              <select
                name="fuel_type"
                onChange={(e) =>
                  setFormData({ ...formData, fuel_type: e.target.value })
                }
              >
                <option value="petrol">Benzină</option>
                <option value="diesel">Diesel</option>
                <option value="electric">Electric</option>
              </select>
            </div>
            <div className="input-group">
              <label>AN</label>
              <input
                type="number"
                name="year"
                value={formData.year}
                onChange={(e) =>
                  setFormData({ ...formData, year: e.target.value })
                }
              />
            </div>
            <div className="input-group">
              <label>KM / AN</label>
              <input
                type="number"
                name="km_per_year"
                value={formData.km_per_year}
                onChange={(e) =>
                  setFormData({ ...formData, km_per_year: e.target.value })
                }
              />
            </div>
            <div className="input-group">
              <label>CONSUM</label>
              <input
                type="number"
                step="0.1"
                name="fuel_consumption"
                value={formData.fuel_consumption}
                onChange={(e) =>
                  setFormData({ ...formData, fuel_consumption: e.target.value })
                }
              />
            </div>
            <div className="input-group">
              <label>MOTOR (cm3)</label>
              <input
                type="number"
                name="engine_capacity"
                value={formData.engine_capacity}
                onChange={(e) =>
                  setFormData({ ...formData, engine_capacity: e.target.value })
                }
              />
            </div>
            <div className="input-group">
              <label>VÂRSTĂ ȘOFER</label>
              <input
                type="number"
                name="driver_age"
                value={formData.driver_age}
                onChange={(e) =>
                  setFormData({ ...formData, driver_age: e.target.value })
                }
              />
            </div>
            <button type="submit" className="full-width" disabled={loading}>
              GENEREAZĂ ANALIZA
            </button>
          </form>
        </div>
      ) : (
        <div className="report-grid">
          <div className="card">
            <h3>📊 Distribuție Costuri</h3>
            <div className="stats-row">
              <div>
                <label>LUNAR</label>
                <div className="stat-value">
                  {result.total.monthly.toFixed(2)} RON
                </div>
              </div>
              <div>
                <label>ANUAL</label>
                <div className="stat-value">
                  {result.total.annual.toFixed(2)} RON
                </div>
              </div>
            </div>
            <div className="income-highlight">
              <label>VENIT MINIM RECOMANDAT</label>
              <div className="income-value">
                {result.income_analysis.safe_minimum_income.toFixed(0)} RON
              </div>
            </div>
            <Chart
              options={donutOptions}
              series={[
                result.fuel.monthly,
                result.insurance.monthly,
                result.maintenance.monthly,
              ]}
              type="donut"
              height={300}
            />
            <button
              onClick={() => setResult(null)}
              style={{
                width: "100%",
                marginTop: "20px",
                background: "#1e293b",
              }}
            >
              Analiză Nouă
            </button>
          </div>

          <div className="card">
            <h3>📈 Proiecție 5 Ani</h3>
            <Chart
              options={areaOptions}
              series={[
                {
                  name: "Cost Total",
                  data: [
                    result.total.annual,
                    result.total.annual * 1.08,
                    result.total.annual * 1.15,
                    result.total.annual * 1.24,
                    result.total.annual * 1.35,
                  ],
                },
              ]}
              type="area"
              height={350}
            />
            <div
              className={`advisor-box ${result.total.monthly / result.income_analysis.safe_minimum_income > 0.3 ? "risk-high" : "risk-low"}`}
            >
              <h4>CarScope Advisor</h4>
              <p>
                Achiziția {formData.brand} {formData.model} este{" "}
                {result.total.monthly /
                  result.income_analysis.safe_minimum_income >
                0.3
                  ? "un risc financiar ridicat."
                  : "o decizie sustenabilă."}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

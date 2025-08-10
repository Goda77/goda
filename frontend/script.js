const form = document.getElementById("sizeForm");
const resultDiv = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  // Extract and validate input values
  const oil_flow_m3h = parseFloat(document.getElementById("oilFlow").value);
  const water_flow_m3h = parseFloat(document.getElementById("waterFlow").value);
  const allowable_liquid_velocity_m_s = parseFloat(
    document.getElementById("velocity").value
  );
  const L_over_D_ratio = parseFloat(document.getElementById("ratio").value);

  if (
    [
      oil_flow_m3h,
      water_flow_m3h,
      allowable_liquid_velocity_m_s,
      L_over_D_ratio,
    ].some((v) => isNaN(v) || v <= 0)
  ) {
    showError("All inputs must be positive numbers.");
    return;
  }

  const payload = {
    oil_flow_m3h,
    water_flow_m3h,
    allowable_liquid_velocity_m_s,
    L_over_D_ratio,
  };

  try {
    const response = await fetch("http://localhost:8000/api/size", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      showError(data.detail || "Unexpected error");
    } else {
      showResult(data);
    }
  } catch (err) {
    showError("Failed to reach backend. Is it running?");
  }
});

function showError(message) {
  resultDiv.classList.remove("hidden");
  resultDiv.className = "card error";
  resultDiv.innerHTML = `<p>${message}</p>`;
}

function showResult(data) {
  resultDiv.classList.remove("hidden");
  resultDiv.className = "card";
  resultDiv.innerHTML = `
    <h2>Results</h2>
    <table>
      <tbody>
        <tr><th>Total Liquid Flow (m³/h)</th><td>${data.total_liquid_flow_m3h}</td></tr>
        <tr><th>Total Liquid Flow (m³/s)</th><td>${data.total_liquid_flow_m3s}</td></tr>
        <tr><th>Required Area (m²)</th><td>${data.required_area_m2}</td></tr>
        <tr><th>Separator Diameter (m)</th><td>${data.diameter_m}</td></tr>
        <tr><th>Separator Length (m)</th><td>${data.length_m}</td></tr>
      </tbody>
    </table>
  `;
}
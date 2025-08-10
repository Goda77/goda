(function () {
  const form = document.getElementById('sizing-form');
  const errorEl = document.getElementById('error');
  const resultsCard = document.getElementById('results-card');
  const resultsEl = document.getElementById('results');
  const calculateBtn = document.getElementById('calculate-btn');

  // Configure your backend URL here
  const API_BASE = 'http://127.0.0.1:8000';

  function toNumber(value) {
    const num = Number(value);
    return Number.isFinite(num) ? num : NaN;
  }

  function validateInputs(values) {
    const errors = [];
    for (const [key, val] of Object.entries(values)) {
      const num = toNumber(val);
      if (!Number.isFinite(num) || num <= 0) {
        errors.push(`${key} must be a positive number`);
      }
    }
    return errors;
  }

  function renderResults(data) {
    const entries = [
      ['Oil flow (m³/h)', data.oil_flow_m3h],
      ['Water flow (m³/h)', data.water_flow_m3h],
      ['Total liquid flow (m³/h)', data.total_liquid_flow_m3h],
      ['Total liquid flow (m³/s)', data.total_liquid_flow_m3s],
      ['Allowable liquid velocity (m/s)', data.allowable_liquid_velocity_m_s],
      ['Required cross-sectional area (m²)', data.required_cross_sectional_area_m2],
      ['Internal diameter (m)', data.internal_diameter_m],
      ['L/D ratio', data.L_over_D_ratio],
      ['Separator length (m)', data.separator_length_m],
    ];

    const rows = entries.map(([k, v]) => {
      const val = typeof v === 'number' ? v.toFixed(6) : String(v);
      return `<tr><th>${k}</th><td>${val}</td></tr>`;
    }).join('');

    resultsEl.innerHTML = `<table>${rows}</table>`;
    resultsCard.style.display = 'block';
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorEl.style.display = 'none';
    resultsCard.style.display = 'none';

    const values = {
      oil_flow_m3h: form.oil_flow_m3h.value,
      water_flow_m3h: form.water_flow_m3h.value,
      allowable_liquid_velocity_m_s: form.allowable_liquid_velocity_m_s.value,
      L_over_D_ratio: form.L_over_D_ratio.value,
    };

    const errors = validateInputs(values);
    if (errors.length) {
      errorEl.textContent = errors.join('; ');
      errorEl.style.display = 'block';
      return;
    }

    calculateBtn.disabled = true;

    try {
      const resp = await fetch(`${API_BASE}/api/size`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          oil_flow_m3h: Number(values.oil_flow_m3h),
          water_flow_m3h: Number(values.water_flow_m3h),
          allowable_liquid_velocity_m_s: Number(values.allowable_liquid_velocity_m_s),
          L_over_D_ratio: Number(values.L_over_D_ratio),
        })
      });

      const data = await resp.json();
      if (!resp.ok) {
        const detail = data && data.detail ? data.detail : 'Unknown error';
        throw new Error(detail);
      }
      renderResults(data);
    } catch (err) {
      errorEl.textContent = err.message || String(err);
      errorEl.style.display = 'block';
    } finally {
      calculateBtn.disabled = false;
    }
  });
})();
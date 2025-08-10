/**
 * Frontend JavaScript for Separator Sizing Calculator
 * Handles form submission, API communication, and UI updates
 */

// API configuration
const API_BASE_URL = 'http://localhost:8000';
const API_ENDPOINT = '/api/size';

// DOM elements
const form = document.getElementById('separatorForm');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const calculateBtn = document.querySelector('.calculate-btn');

// Result display elements
const resultElements = {
    totalFlowM3h: document.getElementById('totalFlowM3h'),
    totalFlowM3s: document.getElementById('totalFlowM3s'),
    crossSectionalArea: document.getElementById('crossSectionalArea'),
    internalDiameter: document.getElementById('internalDiameter'),
    separatorLength: document.getElementById('separatorLength')
};

// Summary display elements
const summaryElements = {
    oilFlow: document.getElementById('summaryOilFlow'),
    waterFlow: document.getElementById('summaryWaterFlow'),
    velocity: document.getElementById('summaryVelocity'),
    ldRatio: document.getElementById('summaryLDRatio')
};

// Error display element
const errorText = document.getElementById('errorText');

/**
 * Initialize the application
 */
function init() {
    // Add form submit event listener
    form.addEventListener('submit', handleFormSubmit);
    
    // Add input validation listeners
    addInputValidation();
    
    console.log('Separator Sizing Calculator initialized');
}

/**
 * Add real-time input validation
 */
function addInputValidation() {
    const inputs = form.querySelectorAll('input[type="number"]');
    
    inputs.forEach(input => {
        input.addEventListener('input', validateInput);
        input.addEventListener('blur', validateInput);
    });
}

/**
 * Validate individual input field
 */
function validateInput(event) {
    const input = event.target;
    const value = parseFloat(input.value);
    const min = parseFloat(input.min);
    
    // Remove previous error styling
    input.classList.remove('error');
    
    // Check if value is valid
    if (input.value === '' || isNaN(value)) {
        input.classList.add('error');
        return false;
    }
    
    // Check if value meets minimum requirement
    if (value < min) {
        input.classList.add('error');
        return false;
    }
    
    return true;
}

/**
 * Validate entire form
 */
function validateForm() {
    const inputs = form.querySelectorAll('input[type="number"]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!validateInput({ target: input })) {
            isValid = false;
        }
    });
    
    return isValid;
}

/**
 * Handle form submission
 */
async function handleFormSubmit(event) {
    event.preventDefault();
    
    // Validate form inputs
    if (!validateForm()) {
        showError('Please fill in all fields with valid positive numbers.');
        return;
    }
    
    // Get form data
    const formData = new FormData(form);
    const inputData = {
        oil_flow_m3h: parseFloat(formData.get('oilFlow')),
        water_flow_m3h: parseFloat(formData.get('waterFlow')),
        allowable_liquid_velocity_m_s: parseFloat(formData.get('liquidVelocity')),
        L_over_D_ratio: parseFloat(formData.get('ldRatio'))
    };
    
    // Show loading state
    setLoadingState(true);
    
    try {
        // Make API call
        const results = await calculateSeparatorSize(inputData);
        
        // Display results
        displayResults(results);
        
        // Hide any previous errors
        hideError();
        
    } catch (error) {
        console.error('Calculation error:', error);
        showError(error.message || 'An error occurred during calculation.');
    } finally {
        // Hide loading state
        setLoadingState(false);
    }
}

/**
 * Make API call to calculate separator size
 */
async function calculateSeparatorSize(inputData) {
    try {
        const response = await fetch(`${API_BASE_URL}${API_ENDPOINT}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(inputData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
        
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            throw new Error('Unable to connect to the server. Please ensure the backend is running on http://localhost:8000');
        }
        throw error;
    }
}

/**
 * Display calculation results
 */
function displayResults(results) {
    // Update result values
    resultElements.totalFlowM3h.textContent = results.total_liquid_flow_m3h;
    resultElements.totalFlowM3s.textContent = results.total_liquid_flow_m3s;
    resultElements.crossSectionalArea.textContent = results.required_cross_sectional_area_m2;
    resultElements.internalDiameter.textContent = results.internal_diameter_m;
    resultElements.separatorLength.textContent = results.separator_length_m;
    
    // Update summary values
    summaryElements.oilFlow.textContent = results.input_parameters.oil_flow_m3h;
    summaryElements.waterFlow.textContent = results.input_parameters.water_flow_m3h;
    summaryElements.velocity.textContent = results.input_parameters.allowable_liquid_velocity_m_s;
    summaryElements.ldRatio.textContent = results.input_parameters.L_over_D_ratio;
    
    // Show results section
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Show error message
 */
function showError(message) {
    errorText.textContent = message;
    errorSection.style.display = 'block';
    
    // Scroll to error
    errorSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Hide error message
 */
function hideError() {
    errorSection.style.display = 'none';
}

/**
 * Set loading state for calculate button
 */
function setLoadingState(isLoading) {
    if (isLoading) {
        calculateBtn.classList.add('calculating');
        calculateBtn.disabled = true;
    } else {
        calculateBtn.classList.remove('calculating');
        calculateBtn.disabled = false;
    }
}

/**
 * Format number for display
 */
function formatNumber(number, decimals = 4) {
    return Number(number).toFixed(decimals);
}

/**
 * Add error styling to CSS
 */
function addErrorStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .form-group input.error {
            border-color: #e74c3c;
            background-color: #fff5f5;
        }
        
        .form-group input.error:focus {
            border-color: #e74c3c;
            box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
        }
    `;
    document.head.appendChild(style);
}

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    addErrorStyles();
    init();
});

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        validateForm,
        calculateSeparatorSize,
        displayResults,
        showError,
        hideError
    };
}
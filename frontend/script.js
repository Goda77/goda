/**
 * Horizontal Three-Phase Separator Sizing Frontend
 * Handles form validation, API communication, and results display
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM elements
const form = document.getElementById('separatorForm');
const calculateBtn = document.getElementById('calculateBtn');
const resultsCard = document.getElementById('resultsCard');
const errorCard = document.getElementById('errorCard');
const loading = document.getElementById('loading');

// Input elements
const oilFlowInput = document.getElementById('oilFlow');
const waterFlowInput = document.getElementById('waterFlow');
const liquidVelocityInput = document.getElementById('liquidVelocity');
const ldRatioInput = document.getElementById('ldRatio');

// Result elements
const totalFlowM3hSpan = document.getElementById('totalFlowM3h');
const totalFlowM3sSpan = document.getElementById('totalFlowM3s');
const crossSectionalAreaSpan = document.getElementById('crossSectionalArea');
const internalDiameterSpan = document.getElementById('internalDiameter');
const separatorLengthSpan = document.getElementById('separatorLength');

// Error message element
const errorMessage = document.getElementById('errorMessage');

/**
 * Validate form inputs
 * @returns {boolean} True if all inputs are valid
 */
function validateInputs() {
    let isValid = true;
    const inputs = [
        { element: oilFlowInput, errorId: 'oilFlowError', name: 'Oil Flow Rate' },
        { element: waterFlowInput, errorId: 'waterFlowError', name: 'Water Flow Rate' },
        { element: liquidVelocityInput, errorId: 'liquidVelocityError', name: 'Allowable Liquid Velocity' },
        { element: ldRatioInput, errorId: 'ldRatioError', name: 'L/D Ratio' }
    ];

    inputs.forEach(input => {
        const errorElement = document.getElementById(input.errorId);
        const value = parseFloat(input.element.value);
        
        // Clear previous error
        errorElement.textContent = '';
        input.element.classList.remove('error');
        
        // Validate
        if (isNaN(value) || value <= 0) {
            errorElement.textContent = `${input.name} must be a positive number`;
            input.element.classList.add('error');
            isValid = false;
        }
    });

    return isValid;
}

/**
 * Show loading state
 */
function showLoading() {
    loading.style.display = 'block';
    resultsCard.style.display = 'none';
    errorCard.style.display = 'none';
    calculateBtn.disabled = true;
}

/**
 * Hide loading state
 */
function hideLoading() {
    loading.style.display = 'none';
    calculateBtn.disabled = false;
}

/**
 * Display calculation results
 * @param {Object} results - Calculation results from API
 */
function displayResults(results) {
    totalFlowM3hSpan.textContent = results.total_liquid_flow_m3h.toFixed(4);
    totalFlowM3sSpan.textContent = results.total_liquid_flow_m3s.toFixed(6);
    crossSectionalAreaSpan.textContent = results.required_cross_sectional_area_m2.toFixed(6);
    internalDiameterSpan.textContent = results.internal_diameter_m.toFixed(4);
    separatorLengthSpan.textContent = results.separator_length_m.toFixed(4);
    
    resultsCard.style.display = 'block';
    errorCard.style.display = 'none';
}

/**
 * Display error message
 * @param {string} message - Error message to display
 */
function displayError(message) {
    errorMessage.textContent = message;
    errorCard.style.display = 'block';
    resultsCard.style.display = 'none';
}

/**
 * Send calculation request to API
 * @param {Object} inputData - Form data to send
 */
async function calculateSeparatorDimensions(inputData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/size`, {
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

        const results = await response.json();
        return results;
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            throw new Error('Unable to connect to the backend server. Please ensure the server is running on http://localhost:8000');
        }
        throw error;
    }
}

/**
 * Handle form submission
 * @param {Event} event - Form submit event
 */
async function handleFormSubmit(event) {
    event.preventDefault();
    
    // Validate inputs
    if (!validateInputs()) {
        return;
    }
    
    // Prepare input data
    const inputData = {
        oil_flow_m3h: parseFloat(oilFlowInput.value),
        water_flow_m3h: parseFloat(waterFlowInput.value),
        allowable_liquid_velocity_m_s: parseFloat(liquidVelocityInput.value),
        L_over_D_ratio: parseFloat(ldRatioInput.value)
    };
    
    showLoading();
    
    try {
        const results = await calculateSeparatorDimensions(inputData);
        displayResults(results);
    } catch (error) {
        displayError(error.message);
    } finally {
        hideLoading();
    }
}

/**
 * Load example data into form
 */
function loadExampleData() {
    oilFlowInput.value = '36';
    waterFlowInput.value = '14';
    liquidVelocityInput.value = '0.3';
    ldRatioInput.value = '3';
}

/**
 * Initialize the application
 */
function init() {
    // Add form submit listener
    form.addEventListener('submit', handleFormSubmit);
    
    // Load example data on page load
    loadExampleData();
    
    // Add input validation on blur
    [oilFlowInput, waterFlowInput, liquidVelocityInput, ldRatioInput].forEach(input => {
        input.addEventListener('blur', validateInputs);
        input.addEventListener('input', () => {
            // Clear error state when user starts typing
            const errorId = input.id + 'Error';
            const errorElement = document.getElementById(errorId);
            if (errorElement) {
                errorElement.textContent = '';
                input.classList.remove('error');
            }
        });
    });
    
    console.log('Separator Sizing Application initialized');
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', init);
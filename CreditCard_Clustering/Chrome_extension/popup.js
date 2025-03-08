document.addEventListener('DOMContentLoaded', function() {
    const predictButton = document.getElementById('predict');
    const resultDiv = document.getElementById('result');

    predictButton.addEventListener('click', async function() {
        // Get input values
        const balance = parseFloat(document.getElementById('balance').value);
        const purchases = parseFloat(document.getElementById('purchases').value);
        const creditLimit = parseFloat(document.getElementById('creditLimit').value);

        // Validate inputs
        if (isNaN(balance) || isNaN(purchases) || isNaN(creditLimit)) {
            showResult('Please fill in all fields with valid numbers', false);
            return;
        }

        // Prepare data for API
        const data = {
            BALANCE: balance,
            PURCHASES: purchases,
            CREDIT_LIMIT: creditLimit
        };

        try {
            // Make API call
            const response = await fetch('http://127.0.0.1:8000/predict_cluster', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error('API request failed');
            }

            const result = await response.json();
            
            // Show result
            const message = `Cluster: ${result.cluster_id}\nDescription: ${result.cluster_description}`;
            showResult(message, true);

        } catch (error) {
            showResult('Error: Could not connect to the API. Make sure the API server is running.', false);
        }
    });

    function showResult(message, isSuccess) {
        resultDiv.textContent = message;
        resultDiv.style.display = 'block';
        resultDiv.className = isSuccess ? 'success' : 'error';
    }
}); 
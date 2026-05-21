// API Service Layer - Handles all HTTP requests to the daemon
// Max 200 LOC per component file

const apiService = {
    baseUrl: window.location.origin,
    
    async request(endpoint, options = {}) {
        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    },
    
    // Status endpoints
    getStatus() {
        return this.request('/api/status');
    },
    
    getHealth() {
        return this.request('/api/health');
    },
    
    getAPIInfo() {
        return this.request('/');
    },
    
    // Generic request method for testing
    testEndpoint(method, endpoint, body = null) {
        const options = {
            method: method.toUpperCase(),
        };
        
        if (body && (method.toUpperCase() === 'POST' || method.toUpperCase() === 'PUT')) {
            options.body = JSON.stringify(body);
        }
        
        return this.request(endpoint, options);
    }
};
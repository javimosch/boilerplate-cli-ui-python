// APITester Component - Interactive API testing interface
// Max 200 LOC per component file

const { useState } = React;

function APITester({ onResponse, onError }) {
    const [method, setMethod] = useState('GET');
    const [endpoint, setEndpoint] = useState('/');
    const [body, setBody] = useState('');
    const [loading, setLoading] = useState(false);
    
    const commonEndpoints = [
        { path: '/', method: 'GET', label: 'API Info' },
        { path: '/api/status', method: 'GET', label: 'Status' },
        { path: '/api/health', method: 'GET', label: 'Health Check' }
    ];
    
    const methods = ['GET', 'POST', 'PUT', 'DELETE'];
    
    const handleQuickTest = (path, httpMethod) => {
        setEndpoint(path);
        setMethod(httpMethod);
        executeTest(path, httpMethod);
    };
    
    const executeTest = async (customEndpoint, customMethod) => {
        const testEndpoint = customEndpoint || endpoint;
        const testMethod = customMethod || method;
        
        setLoading(true);
        try {
            let requestBody = null;
            if (testMethod !== 'GET' && body.trim()) {
                try {
                    requestBody = JSON.parse(body);
                } catch {
                    onError('Invalid JSON in request body');
                    setLoading(false);
                    return;
                }
            }
            
            const response = await apiService.testEndpoint(testMethod, testEndpoint, requestBody);
            onResponse(response);
        } catch (err) {
            onError(err.message);
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <div className="bg-white border border-[#EAEAEA] rounded-xl p-6 card-hover">
            <h2 className="text-lg font-semibold text-[#111111] mb-4">API Tester</h2>
            
            {/* Quick test buttons */}
            <div className="flex flex-wrap gap-2 mb-6">
                {commonEndpoints.map((item) => (
                    <button
                        key={item.path}
                        onClick={() => handleQuickTest(item.path, item.method)}
                        className="px-4 py-2 bg-[#F7F6F3] hover:bg-[#EAEAEA] rounded-lg text-sm font-medium text-[#111111] transition-colors btn-active"
                        disabled={loading}
                    >
                        {item.label}
                    </button>
                ))}
            </div>
            
            {/* Method selector */}
            <div className="mb-4">
                <label className="block text-sm font-medium text-[#787774] mb-2">Method</label>
                <div className="flex gap-2">
                    {methods.map((m) => (
                        <button
                            key={m}
                            onClick={() => setMethod(m)}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors btn-active ${
                                method === m 
                                    ? 'bg-[#111111] text-white' 
                                    : 'bg-[#F7F6F3] text-[#111111] hover:bg-[#EAEAEA]'
                            }`}
                        >
                            {m}
                        </button>
                    ))}
                </div>
            </div>
            
            {/* Endpoint input */}
            <div className="mb-4">
                <label className="block text-sm font-medium text-[#787774] mb-2">Endpoint</label>
                <input
                    type="text"
                    value={endpoint}
                    onChange={(e) => setEndpoint(e.target.value)}
                    className="w-full px-4 py-2 border border-[#EAEAEA] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#111111] mono text-sm"
                    placeholder="/api/endpoint"
                />
            </div>
            
            {/* Request body (for POST/PUT) */}
            {method !== 'GET' && (
                <div className="mb-4">
                    <label className="block text-sm font-medium text-[#787774] mb-2">Request Body (JSON)</label>
                    <textarea
                        value={body}
                        onChange={(e) => setBody(e.target.value)}
                        className="w-full px-4 py-2 border border-[#EAEAEA] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#111111] mono text-sm h-24 resize-none"
                        placeholder='{"key": "value"}'
                    />
                </div>
            )}
            
            {/* Execute button */}
            <button
                onClick={() => executeTest()}
                disabled={loading}
                className="w-full px-4 py-3 bg-[#111111] hover:bg-[#333333] text-white rounded-lg font-medium transition-colors btn-active disabled:opacity-50 disabled:cursor-not-allowed"
            >
                {loading ? (
                    <span className="flex items-center justify-center gap-2">
                        <i data-lucide="loader-2" className="w-5 h-5 animate-spin"></i>
                        Sending...
                    </span>
                ) : 'Send Request'}
            </button>
        </div>
    );
}
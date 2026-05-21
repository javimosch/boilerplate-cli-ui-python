// APITestView - Dedicated API testing interface
// Max 200 LOC per component file

const { useState, useEffect } = React;

function APITestView() {
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);
    const [mounted, setMounted] = useState(false);
    
    useEffect(() => {
        setMounted(true);
        lucide.createIcons();
    }, []);
    
    const handleResponse = (data) => {
        setResponse(data);
        setError(null);
    };
    
    const handleError = (errorMessage) => {
        setError(errorMessage);
        setResponse(null);
    };
    
    return (
        <div className="p-6 lg:p-8 space-y-6">
            {/* Header */}
            <div className="scroll-entry" style={{ animationDelay: '0ms' }}>
                <h1 className="text-2xl font-semibold text-[#111111] mb-2">API Testing</h1>
                <p className="text-[#787774]">Test daemon endpoints with custom requests</p>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* API Tester */}
                <div className="scroll-entry" style={{ animationDelay: '100ms' }}>
                    <APITester 
                        onResponse={handleResponse}
                        onError={handleError}
                    />
                </div>
                
                {/* Response Viewer */}
                <div className="scroll-entry" style={{ animationDelay: '200ms' }}>
                    <ResponseViewer 
                        response={response} 
                        error={error} 
                        loading={false}
                    />
                </div>
            </div>
            
            {/* API Documentation */}
            <div className="scroll-entry" style={{ animationDelay: '300ms' }}>
                <div className="bg-white border border-[#EAEAEA] rounded-xl p-6">
                    <h2 className="text-lg font-semibold text-[#111111] mb-4">Available Endpoints</h2>
                    <div className="space-y-3">
                        {[
                            { method: 'GET', path: '/', description: 'API information and available endpoints' },
                            { method: 'GET', path: '/api/status', description: 'Server status, port, and uptime information' },
                            { method: 'GET', path: '/api/health', description: 'Health check endpoint' }
                        ].map((endpoint, index) => (
                            <div key={index} className="flex items-start gap-4 p-4 bg-[#F7F6F3] rounded-lg">
                                <span className={`px-2 py-1 rounded text-xs font-mono font-medium ${
                                    endpoint.method === 'GET' ? 'bg-[#346538] text-white' : 'bg-[#111111] text-white'
                                }`}>
                                    {endpoint.method}
                                </span>
                                <div className="flex-1">
                                    <code className="mono text-sm text-[#111111]">{endpoint.path}</code>
                                    <p className="text-sm text-[#787774] mt-1">{endpoint.description}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
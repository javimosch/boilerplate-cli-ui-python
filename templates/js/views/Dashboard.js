// Dashboard View - Main dashboard with status and quick actions
// Max 200 LOC per component file

const { useState, useEffect } = React;

function Dashboard() {
    const { status, loading, error, refresh } = useDaemonStatus(5000);
    const [response, setResponse] = useState(null);
    const [apiError, setApiError] = useState(null);
    const [mounted, setMounted] = useState(false);
    
    useEffect(() => {
        setMounted(true);
        lucide.createIcons();
    }, []);
    
    useEffect(() => {
        if (mounted) {
            lucide.createIcons();
        }
    }, [status, mounted]);
    
    const handleQuickAction = async (action) => {
        setApiError(null);
        try {
            let data;
            switch (action) {
                case 'status':
                    data = await apiService.getStatus();
                    break;
                case 'health':
                    data = await apiService.getHealth();
                    break;
                case 'info':
                    data = await apiService.getAPIInfo();
                    break;
                default:
                    return;
            }
            setResponse(data);
        } catch (err) {
            setApiError(err.message);
        }
    };
    
    const quickActions = [
        { id: 'status', label: 'Refresh Status', icon: 'refresh-cw', color: 'bg-[#E1F3FE] text-[#1F6C9F]' },
        { id: 'health', label: 'Health Check', icon: 'heart', color: 'bg-[#EDF3EC] text-[#346538]' },
        { id: 'info', label: 'API Info', icon: 'info', color: 'bg-[#FBF3DB] text-[#956400]' }
    ];
    
    return (
        <div className="p-6 lg:p-8 space-y-6">
            {/* Header */}
            <div className="scroll-entry" style={{ animationDelay: '0ms' }}>
                <h1 className="text-2xl font-semibold text-[#111111] mb-2">Dashboard</h1>
                <p className="text-[#787774]">Monitor and manage your daemon server</p>
            </div>
            
            {/* Status Card */}
            <div className="scroll-entry" style={{ animationDelay: '100ms' }}>
                <StatusCard 
                    status={status} 
                    loading={loading} 
                    error={error}
                    onRefresh={refresh}
                />
            </div>
            
            {/* Quick Actions */}
            <div className="scroll-entry" style={{ animationDelay: '200ms' }}>
                <h2 className="text-lg font-semibold text-[#111111] mb-4">Quick Actions</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {quickActions.map((action) => (
                        <button
                            key={action.id}
                            onClick={() => handleQuickAction(action.id)}
                            className={`p-6 rounded-xl border border-[#EAEAEA] card-hover text-left transition-all btn-active ${action.color}`}
                        >
                            <i data-lucide={action.icon} className="w-6 h-6 mb-3"></i>
                            <span className="font-medium">{action.label}</span>
                        </button>
                    ))}
                </div>
            </div>
            
            {/* Response Viewer */}
            <div className="scroll-entry" style={{ animationDelay: '300ms' }}>
                <ResponseViewer 
                    response={response} 
                    error={apiError} 
                    loading={false}
                />
            </div>
        </div>
    );
}
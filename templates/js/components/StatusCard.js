// StatusCard Component - Displays daemon status information
// Max 200 LOC per component file

const { useState, useEffect } = React;

function StatusCard({ status, loading, error, onRefresh }) {
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
    
    const statusItems = [
        {
            label: 'Status',
            value: status.status,
            color: status.status === 'running' ? 'text-[#346538]' : 
                   status.status === 'stopped' ? 'text-[#9F2F2D]' : 
                   'text-[#787774]',
            icon: status.status === 'running' ? 'activity' : 'alert-circle'
        },
        {
            label: 'Port',
            value: status.port ? status.port.toString() : '-',
            color: 'text-[#111111]',
            icon: 'server'
        },
        {
            label: 'Uptime',
            value: loading ? 'Loading...' : `${Math.floor(status.uptime / 60)}m ${Math.floor(status.uptime % 60)}s`,
            color: 'text-[#111111]',
            icon: 'clock'
        },
        {
            label: 'Health',
            value: status.health,
            color: status.health === 'healthy' ? 'text-[#346538]' : 
                   status.health === 'unhealthy' ? 'text-[#9F2F2D]' : 
                   'text-[#787774]',
            icon: status.health === 'healthy' ? 'heart' : 'heart-off'
        }
    ];
    
    return (
        <div className={`bg-white border border-[#EAEAEA] rounded-xl p-6 card-hover scroll-entry ${mounted ? '' : ''}`}>
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-[#111111]">Server Status</h2>
                <button
                    onClick={onRefresh}
                    className="p-2 hover:bg-[#F7F6F3] rounded-lg transition-colors btn-active"
                    disabled={loading}
                >
                    <i data-lucide={loading ? 'loader-2' : 'refresh-cw'} 
                       className={`w-5 h-5 text-[#787774] ${loading ? 'animate-spin' : ''}`}></i>
                </button>
            </div>
            
            {error ? (
                <div className="bg-[#FDEBEC] text-[#9F2F2D] p-4 rounded-lg mb-4">
                    <div className="flex items-center gap-2">
                        <i data-lucide="alert-circle" className="w-5 h-5"></i>
                        <span className="font-medium">Connection Error</span>
                    </div>
                    <p className="text-sm mt-1">{error}</p>
                </div>
            ) : null}
            
            <div className="space-y-0">
                {statusItems.map((item, index) => (
                    <div 
                        key={item.label}
                        className="flex items-center justify-between py-4 border-b border-[#EAEAEA] last:border-0"
                        style={{ animationDelay: `${index * 100}ms` }}
                    >
                        <div className="flex items-center gap-3">
                            <i data-lucide={item.icon} className="w-5 h-5 text-[#787774]"></i>
                            <span className="text-[#787774] font-medium">{item.label}</span>
                        </div>
                        <span className={`font-semibold ${item.color} mono`}>
                            {item.value}
                        </span>
                    </div>
                ))}
            </div>
        </div>
    );
}
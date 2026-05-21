// useDaemonStatus - Composable for daemon status management
// Max 200 LOC per component file

const { useState, useEffect, useCallback } = React;

function useDaemonStatus(refreshInterval = 5000) {
    const [status, setStatus] = useState({
        status: 'loading',
        port: null,
        uptime: 0,
        startTime: null,
        health: 'loading',
        pid: null
    });
    
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    const fetchStatus = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);
            
            const [statusData, healthData] = await Promise.all([
                apiService.getStatus(),
                apiService.getHealth()
            ]);
            
            setStatus({
                status: statusData.status || 'unknown',
                port: statusData.port || null,
                uptime: statusData.uptime_seconds || 0,
                startTime: statusData.start_time || null,
                health: healthData.status || 'unknown',
                pid: statusData.pid || null
            });
        } catch (err) {
            setError(err.message);
            setStatus(prev => ({ ...prev, status: 'error', health: 'error' }));
        } finally {
            setLoading(false);
        }
    }, []);
    
    const refresh = useCallback(() => {
        fetchStatus();
    }, [fetchStatus]);
    
    useEffect(() => {
        fetchStatus();
        
        const interval = setInterval(fetchStatus, refreshInterval);
        
        return () => clearInterval(interval);
    }, [fetchStatus, refreshInterval]);
    
    const formatUptime = (seconds) => {
        if (seconds < 60) return `${seconds.toFixed(1)}s`;
        if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${(seconds % 60).toFixed(0)}s`;
        return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`;
    };
    
    const getStatusColor = (status) => {
        switch (status) {
            case 'running': return 'text-[#346538]';
            case 'stopped': return 'text-[#9F2F2D]';
            case 'loading': return 'text-[#787774]';
            default: return 'text-[#111111]';
        }
    };
    
    const getHealthColor = (health) => {
        switch (health) {
            case 'healthy': return 'text-[#346538]';
            case 'unhealthy': return 'text-[#9F2F2D]';
            case 'loading': return 'text-[#787774]';
            default: return 'text-[#111111]';
        }
    };
    
    return {
        status,
        loading,
        error,
        refresh,
        formatUptime,
        getStatusColor,
        getHealthColor
    };
}
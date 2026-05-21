// ResponseViewer Component - Displays API responses
// Max 200 LOC per component file

const { useState, useEffect, useRef } = React;

function ResponseViewer({ response, error, loading }) {
    const [copied, setCopied] = useState(false);
    const preRef = useRef(null);
    
    useEffect(() => {
        if (preRef.current) {
            preRef.current.scrollTop = 0;
        }
    }, [response]);
    
    const copyToClipboard = () => {
        if (response) {
            navigator.clipboard.writeText(JSON.stringify(response, null, 2));
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        }
    };
    
    const formatJSON = (data) => {
        try {
            return JSON.stringify(data, null, 2);
        } catch {
            return String(data);
        }
    };
    
    return (
        <div className="bg-[#1e1e1e] rounded-xl overflow-hidden">
            <div className="flex items-center justify-between px-4 py-3 bg-[#252526] border-b border-[#333333]">
                <div className="flex items-center gap-2">
                    <i data-lucide="code-2" className="w-5 h-5 text-[#d4d4d4]"></i>
                    <h3 className="text-sm font-medium text-[#d4d4d4]">Response</h3>
                </div>
                {response && (
                    <button
                        onClick={copyToClipboard}
                        className="flex items-center gap-2 px-3 py-1.5 bg-[#333333] hover:bg-[#404040] rounded-lg transition-colors text-xs text-[#d4d4d4] btn-active"
                    >
                        <i data-lucide={copied ? 'check' : 'copy'} className="w-4 h-4"></i>
                        {copied ? 'Copied' : 'Copy'}
                    </button>
                )}
            </div>
            
            <div 
                ref={preRef}
                className="p-4 overflow-auto max-h-[300px] custom-scrollbar"
            >
                {loading ? (
                    <div className="flex items-center justify-center py-8">
                        <i data-lucide="loader-2" className="w-6 h-6 text-[#d4d4d4] animate-spin"></i>
                    </div>
                ) : error ? (
                    <div className="text-[#f87171] mono text-sm">
                        <div className="flex items-center gap-2 mb-2">
                            <i data-lucide="alert-circle" className="w-5 h-5"></i>
                            <span className="font-medium">Error</span>
                        </div>
                        <p>{error}</p>
                    </div>
                ) : response ? (
                    <pre className="mono text-sm text-[#d4d4d4] whitespace-pre-wrap">
                        {formatJSON(response)}
                    </pre>
                ) : (
                    <div className="text-[#787774] text-sm py-8 text-center">
                        <i data-lucide="mouse-pointer-click" className="w-8 h-8 mx-auto mb-2 opacity-50"></i>
                        <p>Click a button to see the response</p>
                    </div>
                )}
            </div>
        </div>
    );
}
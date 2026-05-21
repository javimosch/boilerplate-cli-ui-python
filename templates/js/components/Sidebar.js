// Sidebar Component - Navigation sidebar
// Max 200 LOC per component file

const { Link, useLocation } = ReactRouterDOM;

function Sidebar({ isOpen, onClose }) {
    const location = useLocation();
    
    const navItems = [
        { path: '#/', label: 'Dashboard', icon: 'layout-dashboard' },
        { path: '#/api-test', label: 'API Test', icon: 'code-2' },
        { path: '#/settings', label: 'Settings', icon: 'settings' }
    ];
    
    const isActive = (path) => {
        return location.hash === path || (path === '#/' && location.hash === '');
    };
    
    return (
        <>
            {/* Mobile overlay */}
            {isOpen && (
                <div 
                    className="fixed inset-0 bg-black/50 z-40 lg:hidden"
                    onClick={onClose}
                />
            )}
            
            {/* Sidebar */}
            <aside className={`
                fixed lg:relative inset-y-0 left-0 z-50 lg:z-auto
                w-64 h-full bg-white border-r border-[#EAEAEA]
                transform transition-transform duration-300 ease-in-out flex-shrink-0
                flex flex-col
                ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
            `}>
                {/* Logo */}
                <div className="p-6 border-b border-[#EAEAEA]">
                    <div className="flex items-center gap-3">
                        <div className="w-8 h-8 bg-[#111111] rounded-lg flex items-center justify-center">
                            <i data-lucide="terminal" className="w-5 h-5 text-white"></i>
                        </div>
                        <div>
                            <h1 className="font-semibold text-[#111111]">CLI UI</h1>
                            <p className="text-xs text-[#787774]">Daemon Monitor</p>
                        </div>
                    </div>
                </div>
                
                {/* Navigation */}
                <nav className="p-4">
                    <ul className="space-y-1">
                        {navItems.map((item) => (
                            <li key={item.path}>
                                <Link
                                    to={item.path}
                                    onClick={onClose}
                                    className={`
                                        flex items-center gap-3 px-4 py-3 rounded-lg
                                        transition-all duration-200
                                        ${isActive(item.path) 
                                            ? 'bg-[#F7F6F3] text-[#111111] font-medium' 
                                            : 'text-[#787774] hover:bg-[#F7F6F3] hover:text-[#111111]'
                                        }
                                    `}
                                >
                                    <i data-lucide={item.icon} className="w-5 h-5"></i>
                                    <span>{item.label}</span>
                                </Link>
                            </li>
                        ))}
                    </ul>
                </nav>
                
                {/* Status indicator */}
                <div className="mt-auto p-4 border-t border-[#EAEAEA]">
                    <div className="flex items-center gap-3 px-4 py-3 bg-[#EDF3EC] rounded-lg">
                        <div className="w-2 h-2 bg-[#346538] rounded-full animate-pulse"></div>
                        <span className="text-sm text-[#346538] font-medium">Daemon Active</span>
                    </div>
                </div>
            </aside>
        </>
    );
}
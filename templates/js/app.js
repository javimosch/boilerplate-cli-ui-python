// Main App Component - Root application with routing
// Max 500 LOC per module file

const { HashRouter, Routes, Route, Navigate } = ReactRouterDOM;

function App() {
    const [sidebarOpen, setSidebarOpen] = React.useState(false);
    const [mounted, setMounted] = React.useState(false);
    
    React.useEffect(() => {
        setMounted(true);
        lucide.createIcons();
    }, []);
    
    React.useEffect(() => {
        if (mounted) {
            lucide.createIcons();
        }
    }, [sidebarOpen, mounted]);
    
    return (
        <HashRouter>
            <div className="min-h-screen bg-[#F7F6F3] flex flex-col">
                {/* Mobile Header */}
                <div className="lg:hidden">
                    <MobileHeader onMenuClick={() => setSidebarOpen(true)} />
                </div>
                
                <div className="flex flex-1 overflow-hidden">
                    {/* Sidebar */}
                    <Sidebar 
                        isOpen={sidebarOpen} 
                        onClose={() => setSidebarOpen(false)} 
                    />
                    
                    {/* Main Content */}
                    <main className="flex-1 overflow-auto pt-16 lg:pt-0">
                        <Routes>
                            <Route path="/" element={<Dashboard />} />
                            <Route path="/api-test" element={<APITestView />} />
                            <Route path="/settings" element={<SettingsView />} />
                            <Route path="*" element={<Navigate to="/" replace />} />
                        </Routes>
                    </main>
                </div>
            </div>
        </HashRouter>
    );
}

// Render the app
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
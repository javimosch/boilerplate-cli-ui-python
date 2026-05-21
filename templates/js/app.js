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
            <div className="min-h-screen bg-[#F7F6F3]">
                {/* Mobile Header */}
                <MobileHeader onMenuClick={() => setSidebarOpen(true)} />
                
                {/* Sidebar */}
                <Sidebar 
                    isOpen={sidebarOpen} 
                    onClose={() => setSidebarOpen(false)} 
                />
                
                {/* Main Content */}
                <main className="lg:ml-64 pt-16 lg:pt-0 min-h-screen">
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/api-test" element={<APITestView />} />
                        <Route path="/settings" element={<SettingsView />} />
                        <Route path="*" element={<Navigate to="/" replace />} />
                    </Routes>
                </main>
            </div>
        </HashRouter>
    );
}

// Render the app
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
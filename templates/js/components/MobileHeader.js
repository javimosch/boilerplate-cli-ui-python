// MobileHeader Component - Mobile navigation header
// Max 200 LOC per component file

function MobileHeader({ onMenuClick }) {
    return (
        <header className="lg:hidden fixed top-0 left-0 right-0 bg-white border-b border-[#EAEAEA] z-30">
            <div className="flex items-center justify-between px-4 py-3">
                <div className="flex items-center gap-3">
                    <button
                        onClick={onMenuClick}
                        className="p-2 hover:bg-[#F7F6F3] rounded-lg transition-colors btn-active"
                    >
                        <i data-lucide="menu" className="w-6 h-6 text-[#111111]"></i>
                    </button>
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 bg-[#111111] rounded-lg flex items-center justify-center">
                            <i data-lucide="terminal" className="w-5 h-5 text-white"></i>
                        </div>
                        <div>
                            <h1 className="font-semibold text-[#111111] text-sm">CLI UI</h1>
                            <p className="text-xs text-[#787774]">Daemon Monitor</p>
                        </div>
                    </div>
                </div>
                
                <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-[#346538] rounded-full animate-pulse"></div>
                </div>
            </div>
        </header>
    );
}
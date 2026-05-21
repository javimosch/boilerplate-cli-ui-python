// SettingsView - Configuration and settings interface
// Max 200 LOC per component file

const { useState, useEffect } = React;

function SettingsView() {
    const [mounted, setMounted] = useState(false);
    const [settings, setSettings] = useState({
        refreshInterval: 5000,
        theme: 'light',
        notifications: true
    });
    
    useEffect(() => {
        setMounted(true);
        lucide.createIcons();
    }, []);
    
    const handleSettingChange = (key, value) => {
        setSettings(prev => ({ ...prev, [key]: value }));
    };
    
    const settingSections = [
        {
            title: 'Display',
            items: [
                {
                    key: 'theme',
                    label: 'Theme',
                    type: 'select',
                    options: ['light', 'dark'],
                    description: 'Choose your preferred color scheme'
                },
                {
                    key: 'refreshInterval',
                    label: 'Refresh Interval',
                    type: 'select',
                    options: [1000, 5000, 10000, 30000],
                    formatLabel: (val) => `${val/1000}s`,
                    description: 'How often to refresh daemon status'
                }
            ]
        },
        {
            title: 'Notifications',
            items: [
                {
                    key: 'notifications',
                    label: 'Enable Notifications',
                    type: 'toggle',
                    description: 'Show desktop notifications for status changes'
                }
            ]
        }
    ];
    
    return (
        <div className="p-6 lg:p-8 space-y-6">
            {/* Header */}
            <div className="scroll-entry" style={{ animationDelay: '0ms' }}>
                <h1 className="text-2xl font-semibold text-[#111111] mb-2">Settings</h1>
                <p className="text-[#787774]">Configure your UI preferences</p>
            </div>
            
            {settingSections.map((section, sectionIndex) => (
                <div 
                    key={section.title}
                    className="scroll-entry bg-white border border-[#EAEAEA] rounded-xl p-6"
                    style={{ animationDelay: `${(sectionIndex + 1) * 100}ms` }}
                >
                    <h2 className="text-lg font-semibold text-[#111111] mb-4">{section.title}</h2>
                    <div className="space-y-4">
                        {section.items.map((item) => (
                            <div key={item.key} className="flex items-start justify-between py-3 border-b border-[#EAEAEA] last:border-0">
                                <div className="flex-1">
                                    <label className="block font-medium text-[#111111] mb-1">
                                        {item.label}
                                    </label>
                                    <p className="text-sm text-[#787774]">{item.description}</p>
                                </div>
                                
                                <div className="ml-4">
                                    {item.type === 'select' ? (
                                        <select
                                            value={settings[item.key]}
                                            onChange={(e) => handleSettingChange(item.key, 
                                                item.key === 'refreshInterval' ? parseInt(e.target.value) : e.target.value
                                            )}
                                            className="px-4 py-2 border border-[#EAEAEA] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#111111] bg-white text-sm"
                                        >
                                            {item.options.map((option) => (
                                                <option key={option} value={option}>
                                                    {item.formatLabel ? item.formatLabel(option) : option}
                                                </option>
                                            ))}
                                        </select>
                                    ) : item.type === 'toggle' ? (
                                        <button
                                            onClick={() => handleSettingChange(item.key, !settings[item.key])}
                                            className={`relative w-12 h-6 rounded-full transition-colors ${
                                                settings[item.key] ? 'bg-[#346538]' : 'bg-[#EAEAEA]'
                                            }`}
                                        >
                                            <span className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${
                                                settings[item.key] ? 'translate-x-6' : 'translate-x-1'
                                            }`} />
                                        </button>
                                    ) : null}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            ))}
            
            {/* Info Section */}
            <div className="scroll-entry bg-white border border-[#EAEAEA] rounded-xl p-6" style={{ animationDelay: '300ms' }}>
                <h2 className="text-lg font-semibold text-[#111111] mb-4">About</h2>
                <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                        <span className="text-[#787774]">Version</span>
                        <span className="mono text-[#111111]">1.0.0</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-[#787774]">React Version</span>
                        <span className="mono text-[#111111]">18.0.0</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-[#787774]">Router</span>
                        <span className="mono text-[#111111]">Hashbang</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
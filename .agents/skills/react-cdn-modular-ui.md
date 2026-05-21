# React CDN Modular UI Development

Use this skill when building React applications via CDN with modular architecture and hashbang routing.

## Technical Stack

### Core Dependencies
- **React 18** via CDN (`unpkg.com/react@18/umd/react.development.js`)
- **React DOM** via CDN (`unpkg.com/react-dom@18/umd/react-dom.development.js`)
- **React Router** via CDN (`unpkg.com/react-router-dom@6.3.0/umd/react-router-dom.development.js`)
- **Babel** for JSX transformation (`unpkg.com/@babel/standalone/babel.min.js`)
- **Tailwind CSS** via CDN (`cdn.tailwindcss.com`)
- **Lucide Icons** via CDN (`unpkg.com/lucide@latest`)

### File Structure (LOC Limits)
```
templates/
├── index.html (main HTML, max 150 LOC)
└── js/
    ├── app.js (main app + routing, max 500 LOC)
    ├── services/ (API calls, max 200 LOC each)
    ├── composables/ (state management, max 200 LOC each)
    ├── components/ (reusable UI, max 200 LOC each)
    └── views/ (page components, max 200 LOC each)
```

## Layout Architecture

### Flex Layout Pattern
**Critical**: Use flexbox for proper sidebar/content alignment and scrolling

```javascript
// Correct layout structure
<div className="min-h-screen bg-[#F7F6F3] flex flex-col">
    {/* Mobile Header */}
    <div className="lg:hidden">
        <MobileHeader />
    </div>
    
    <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <Sidebar />
        
        {/* Main Content */}
        <main className="flex-1 overflow-auto pt-16 lg:pt-0">
            <Routes>
                <Route path="/" element={<Dashboard />} />
            </Routes>
        </main>
    </div>
</div>
```

### Common Layout Pitfalls

**Pitfall**: Using fixed positioning for layout structure
```javascript
// WRONG - breaks scrolling and alignment
<aside className="fixed inset-y-0 left-0">
<main className="ml-64">
```

**Solution**: Use flex layout with proper overflow
```javascript
// CORRECT - proper scrolling and alignment
<div className="flex flex-1 overflow-hidden">
    <aside className="lg:relative w-64 flex-shrink-0">
    <main className="flex-1 overflow-auto">
```

**Pitfall**: Missing overflow handling on main content
```javascript
// WRONG - content extends beyond viewport
<main className="flex-1">
```

**Solution**: Add overflow for independent scrolling
```javascript
// CORRECT - content scrolls independently
<main className="flex-1 overflow-auto">
```

## Component Architecture

### Service Layer (API Calls)
**Purpose**: Isolate HTTP requests and API interactions
**Max LOC**: 200 per service file

```javascript
const apiService = {
    baseUrl: window.location.origin,
    
    async request(endpoint, options = {}) {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            headers: { 'Content-Type': 'application/json' },
            ...options
        });
        return await response.json();
    },
    
    getStatus() { return this.request('/api/status'); }
};
```

### Composable Layer (State Management)
**Purpose**: Reusable state logic and side effects
**Max LOC**: 200 per composable

```javascript
function useDaemonStatus(refreshInterval = 5000) {
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(true);
    
    const fetchStatus = useCallback(async () => {
        setLoading(true);
        try {
            const data = await apiService.getStatus();
            setStatus(data);
        } finally {
            setLoading(false);
        }
    }, []);
    
    useEffect(() => {
        fetchStatus();
        const interval = setInterval(fetchStatus, refreshInterval);
        return () => clearInterval(interval);
    }, [fetchStatus, refreshInterval]);
    
    return { status, loading, refresh: fetchStatus };
}
```

### Component Layer (Reusable UI)
**Purpose**: Presentational components with minimal logic
**Max LOC**: 200 per component

```javascript
function StatusCard({ status, loading, onRefresh }) {
    const [mounted, setMounted] = useState(false);
    
    useEffect(() => {
        setMounted(true);
        lucide.createIcons();
    }, []);
    
    return (
        <div className={`bg-white border rounded-xl p-6 scroll-entry ${mounted ? '' : ''}`}>
            {/* Component content */}
        </div>
    );
}
```

## Hashbang Routing

### Router Setup
```javascript
const { HashRouter, Routes, Route, Navigate } = ReactRouterDOM;

function App() {
    return (
        <HashRouter>
            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/api-test" element={<APITestView />} />
                <Route path="/settings" element={<SettingsView />} />
                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
        </HashRouter>
    );
}
```

### Navigation Pattern
```javascript
const { Link } = ReactRouterDOM;

function Sidebar() {
    return (
        <nav>
            <Link to="#/">Dashboard</Link>
            <Link to="#/api-test">API Test</Link>
            <Link to="#/settings">Settings</Link>
        </nav>
    );
}
```

### Full Reload Support
- Each route must be accessible via direct URL
- No client-only state that breaks on refresh
- Use URL parameters for view state when needed
- Test routing with browser back/forward buttons

## Performance Optimization

### React Performance Patterns
```javascript
// Use useCallback for event handlers
const handleClick = useCallback(() => {
    doSomething();
}, [dependencies]);

// Use useMemo for expensive computations
const expensiveValue = useMemo(() => {
    return computeExpensiveValue(data);
}, [data]);

// Cleanup in useEffect
useEffect(() => {
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
}, []);
```

### Icon Management
```javascript
// Initialize Lucide icons after component mount
useEffect(() => {
    lucide.createIcons();
}, []);

// Re-initialize when dynamic content changes
useEffect(() => {
    if (mounted) {
        lucide.createIcons();
    }
}, [dynamicContent, mounted]);
```

### Loading States
```javascript
// Show loading state during async operations
{loading ? (
    <div className="flex items-center justify-center">
        <i data-lucide="loader-2" className="w-6 h-6 animate-spin"></i>
    </div>
) : (
    <div>{content}</div>
)}
```

## Mobile Responsiveness

### Mobile Navigation Pattern
```javascript
function App() {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    
    return (
        <div className="flex flex-col">
            {/* Mobile header only */}
            <div className="lg:hidden">
                <MobileHeader onMenuClick={() => setSidebarOpen(true)} />
            </div>
            
            <div className="flex flex-1 overflow-hidden">
                <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
                <main className="flex-1 overflow-auto pt-16 lg:pt-0">
                    {/* Content */}
                </main>
            </div>
        </div>
    );
}
```

### Responsive Sidebar
```javascript
// Mobile: fixed with overlay, Desktop: relative
<aside className={`
    fixed lg:relative inset-y-0 left-0 z-50 lg:z-auto
    w-64 h-full bg-white border-r
    transform transition-transform
    ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
`}>
```

### Mobile Drawer Overlay
```javascript
{isOpen && (
    <div 
        className="fixed inset-0 bg-black/50 z-40 lg:hidden"
        onClick={onClose}
    />
)}
```

## Error Handling

### API Error Handling
```javascript
const [error, setError] = useState(null);

const fetchData = async () => {
    try {
        const data = await apiService.getData();
        setData(data);
        setError(null);
    } catch (err) {
        setError(err.message);
        setData(null);
    }
};
```

### Error Display Pattern
```javascript
{error ? (
    <div className="bg-[#FDEBEC] text-[#9F2F2D] p-4 rounded-lg">
        <div className="flex items-center gap-2">
            <i data-lucide="alert-circle" className="w-5 h-5"></i>
            <span className="font-medium">Error</span>
        </div>
        <p className="text-sm mt-1">{error}</p>
    </div>
) : null}
```

## Styling Guidelines

### Tailwind CDN Configuration
```javascript
// In HTML head
<script src="https://cdn.tailwindcss.com"></script>

// Custom colors in style tag
<style>
:root {
    --canvas: #F7F6F3;
    --surface: #FFFFFF;
    --border: #EAEAEA;
}
</style>
```

### Minimalist Design Principles
- Use warm monochrome palette
- Ultra-light borders (`#EAEAEA`)
- Subtle shadows (`box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04)`)
- Proper whitespace and typography hierarchy
- No heavy gradients or neon colors

### Animation Patterns
```css
/* Scroll entry animation */
.scroll-entry {
    animation: fadeSlideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    opacity: 0;
    transform: translateY(12px);
}

@keyframes fadeSlideUp {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

## Common Pitfalls

### CDN Script Loading Order
**Pitfall**: Scripts load in wrong order causing undefined errors
**Solution**: Load dependencies in correct order: React → Router → Babel → App → Services → Components → Views

### Icon Rendering Issues
**Pitfall**: Icons don't appear after dynamic content updates
**Solution**: Call `lucide.createIcons()` after content updates in useEffect

### Memory Leaks in Intervals
**Pitfall**: Intervals not cleaned up cause memory leaks
**Solution**: Always return cleanup function in useEffect

```javascript
useEffect(() => {
    const interval = setInterval(callback, 1000);
    return () => clearInterval(interval); // Critical cleanup
}, []);
```

### State Management Issues
**Pitfall**: Direct state mutations cause re-render issues
**Solution**: Always use setState or immer for immutable updates

## Testing Checklist

### Functional Testing
- [ ] All routes accessible via direct URL
- [ ] Hashbang routing works with browser navigation
- [ ] Mobile drawer opens/closes correctly
- [ ] Content scrolls independently of sidebar
- [ ] API calls handle errors gracefully
- [ ] Loading states display correctly
- [ ] Icons render after dynamic updates
- [ ] Responsive design works on all breakpoints

### Performance Testing
- [ ] No memory leaks in long-running sessions
- [ ] Intervals clean up properly on unmount
- [ ] Re-renders minimized with useCallback/useMemo
- [ ] Images and assets optimized
- [ ] CDN scripts load efficiently
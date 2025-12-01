/* static/portfolio/js/tailwind_config.js */
tailwind.config = {
    darkMode: 'class',
    theme: {
        extend: {
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                mono: ['JetBrains Mono', 'monospace'],
            },
            colors: {
                bg: '#0f172a',       /* Slate 900 */
                card: '#1e293b',     /* Slate 800 */
                primary: '#38bdf8',  /* Sky 400 */
                secondary: '#94a3b8',/* Slate 400 */
                accent: '#818cf8',   /* Indigo 400 */
            },
            animation: {
                'spin-slow': 'spin 12s linear infinite',
            }
        }
    }
}
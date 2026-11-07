import { useState, useEffect } from 'react'

export function useTheme() {
    const [refresh, setRefresh] = useState(false)
    const [theme, setTheme] = useState(() => {
        try {
            const stored = localStorage.getItem('theme')
            if (stored) {return stored;} else {return 'light';}
        } catch {return 'sys'} // if localStorage call throws, defaults to system setting
    });

    useEffect(() => {
        const page = window.document.documentElement.classList;
        try {
            if (theme == 'dark') {
                page.add('dark');
                localStorage.setItem('theme', 'dark');
            } else if (theme == 'light') {
                page.remove('dark');
                localStorage.setItem('theme', 'light')
            } else { // theme == 'sys'
                const setting = window.matchMedia('(prefers-color-scheme: dark)').matches;
                if (setting) {
                    page.add('dark');
                } else {
                    page.remove('dark');
                }
                localStorage.setItem('theme', 'sys')
            }
        } catch {page.remove('dark')}
    }, [theme, refresh]);

    useEffect(() => {
        const query = window.matchMedia('(prefers-color-scheme: dark)')
        const update = () => {setRefresh(!refresh)} 

        query.addEventListener('change', update);
        return () => query.removeEventListener('change', update);
    }, [window.matchMedia('(prefers-color-scheme: dark)')]);

    return { theme, setTheme };
}
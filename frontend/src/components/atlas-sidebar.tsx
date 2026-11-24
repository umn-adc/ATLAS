import { Sidebar, SidebarContent, SidebarFooter, SidebarGroup, SidebarGroupContent, SidebarGroupLabel, SidebarHeader } from '@/components/ui/sidebar'
import { Link } from '@tanstack/react-router'
import { ChartArea, ChevronsUpDown, Database, GitBranch, GitGraph, Grid2X2, List, Settings, Shield } from 'lucide-react'
import AtlasLogo from '../assets/atlas-logo.svg';

const AtlasSidebar = () => {
    const username = 'Atlas';
    const email = 'admin@atlas.io';

    const nav = [
        {
            title: 'Monitor',
            items: [
                { label: 'Overview', to: '/', Icon: Grid2X2 },
                { label: 'Strategies', to: '/strategies', Icon: GitGraph },
                { label: 'Deployments', to: '/deployments', Icon: GitBranch }
            ]
        },
        {
            title: 'Tools',
            items: [
                { label: 'Data', to: '/data', Icon: Database },
                { label: 'Backtesting', to: '/backtesting', Icon: ChartArea },
                { label: 'Monitoring', to: '/monitoring', Icon: ChartArea }
            ]
        }, {
            title: 'System',
            items: [
                { label: 'Risk', to: '/risk', Icon: Shield },
                { label: 'Logs', to: '/logs', Icon: List },
                { label: 'Settings', to: '/settings', Icon: Settings }
            ]
        }
    ];

    return (
        <Sidebar>
            <SidebarHeader>
                <Link to={'/'} className='flex flex-row items-center gap-4'>
                    <img src={AtlasLogo} alt="My Logo" width="48" height="48" />
                    <p className='font-brand text-brand text-primary-500'>ATLAS</p>
                </Link>
            </SidebarHeader >

            <SidebarContent>
                {nav.map((group, index) => (
                    <SidebarGroup key={index}>
                        <SidebarGroupLabel className='uppercase tracking-widest'>{group.title}</SidebarGroupLabel>
                        <div className='flex flex-col mt-2'>
                            {group.items.map(item => (
                                <SidebarGroupContent key={item.to}><Link to={item.to} className='flex flex-row items-center gap-2 px-4 py-3 rounded-xl hover:bg-primary-300/10 active:bg-primary-300/20' activeProps={{ className: 'bg-primary-500/10 text-primary-400 font-bold' }}><item.Icon className='size-6' />{item.label}</Link></SidebarGroupContent>
                            ))}
                        </div>
                    </SidebarGroup>
                ))}

            </SidebarContent>

            <SidebarFooter>
                {/* This is a button! I just didn't like shadcn's button and I didn't want to mess with it */}
                <div className='flex items-center gap-2 py-2 px-3 cursor-pointer hover:bg-gray-200 rounded-xl'>
                    <div className='flex size-12  shrink-0 items-center justify-center rounded-full bg-primary-500 text-sm text-white font-bold select-none'>
                        {username.substring(0, 2).toUpperCase()}
                    </div>

                    <div className='flex flex-col'>
                        <p className='font-medium text-lg'>{username}</p>
                        <p className='text-sm text-gray-400'>{email}</p>
                    </div>

                    <div className='ml-auto'>
                        <ChevronsUpDown className='size-6 text-gray-600' />
                    </div>
                </div>
            </SidebarFooter>
        </Sidebar>
    )
}

export default AtlasSidebar
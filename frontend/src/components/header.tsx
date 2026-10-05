import { SidebarTrigger } from '@/components/ui/sidebar';

export default function Header() {
    return (
        <div className='w-full bg-gray-500 h-12'>
            <SidebarTrigger className="absolute m-4" />
        </div>
    );
}
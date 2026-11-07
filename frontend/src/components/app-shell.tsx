import Header from './header';
import Footer from './footer';
import AtlasSidebar from './atlas-sidebar';
import { SidebarProvider } from '@/components/ui/sidebar';

export default function AppShell({ children }: { children: React.ReactNode }) {
    return (
        <SidebarProvider>
            <AtlasSidebar />
            <div className="flex flex-col w-full">
                <Header />
                {children}
                <Footer />
            </div>
        </SidebarProvider>
    );
}
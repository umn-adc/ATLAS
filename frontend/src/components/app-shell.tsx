import Header from './header';
import Footer from './footer';
import AtlasSidebar from './atlas-sidebar';
import { SidebarProvider } from '@/components/ui/sidebar';

export default function AppShell({ children }: { children: React.ReactNode }) {
    return (
        <SidebarProvider>
            <div className="flex flex-col">
                <Header />
                <AtlasSidebar />

                {children}
                <Footer />
            </div>
        </SidebarProvider>
    );
}

import Header from './header';
import Footer from './footer';
import AppSidebar from './app-sidebar';

export default function AppShell({ children }: { children: React.ReactNode }) {
    return (
        <div className="flex flex-column">
            <Header />
            <div className="flex flex-row">
                <AppSidebar />
                {children}
            </div>
            <Footer />
        </div>
    );
}
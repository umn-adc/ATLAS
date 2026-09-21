
import Header from './header';
import Footer from './footer';

export default function AppShell({ children }: { children: React.ReactNode }) {
    return (
        <div className="flex flex-column">
            <Header />
            {children}
            <Footer />
        </div>
    );
}
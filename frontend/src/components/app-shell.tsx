import Header from './header';
import Footer from './footer';

export default function AppShell({ children }: { children: React.ReactNode }) {
    return (
        <div className="flex flex-col">
            <Header />
                {children}
            <Footer />
        </div>
    );
}
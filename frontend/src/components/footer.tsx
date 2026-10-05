
export default function Footer() {
    return (
        <footer className="flex justify-between items-center gap-8 p-4">
            <p>© 2026 ATLAS ™. All Rights Reserved</p>

            <div className="flex gap-6">
                <a href="/privacy">Privacy Policy</a>
                <a href="/terms">Terms and Conditions</a>
                <a href="/contact">Contact</a>
                <a href="/about">About</a>
                <a href="/docs">Docs</a>
                <a href="/research">Research</a>
            </div>
        </footer>
    );
}
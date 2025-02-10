import Link from 'next/link';

export function Header() {
  return (
    <header className="bg-white shadow-sm">
      <nav className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link href="/" className="font-bold text-xl">
            Your Logo
          </Link>
          <div className="space-x-4">
            {/* Add more navigation links as needed */}
          </div>
        </div>
      </nav>
    </header>
  );
} 
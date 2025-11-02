import "./globals.css";

export const metadata = {
  title: "Anime Recommender System",
  description: "Discover your next favorite anime!",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[var(--color-bg)] text-[var(--color-text)] flex flex-col">
        {/* Header */}
        <header className="w-full bg-gradient-to-r from-indigo-500 via-pink-500 to-purple-600 py-6 shadow-lg">
          <h1 className="text-3xl sm:text-4xl font-extrabold text-center text-white tracking-wide">
            🎌 Anime Recommender System
          </h1>
          <p className="text-center text-sm sm:text-base text-indigo-100 mt-1">
            Discover your next favorite anime with AI-powered recommendations!
          </p>
        </header>

        {/* Main Content */}
        <main className="flex-grow">{children}</main>

        {/* Footer */}
        <footer className="py-4 text-center text-sm text-[var(--color-muted)] border-t border-gray-700/30 mt-10">
          © {new Date().getFullYear()} Anime Recommender — Built with ❤️ and AI
        </footer>
      </body>
    </html>
  );
}

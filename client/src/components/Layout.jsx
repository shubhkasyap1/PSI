export default function Layout({ children }) {
  return (
    <div className="flex h-screen bg-zinc-950 text-white">
      
      {/* Sidebar */}
      <aside className="w-64 bg-zinc-900 border-r border-zinc-800 p-4">
        <h2 className="text-lg font-semibold mb-6">AI Doc Q&A</h2>

        <nav className="space-y-3 text-zinc-300">
          <p className="hover:text-white cursor-pointer">Dashboard</p>
          <p className="hover:text-white cursor-pointer">Upload</p>
          <p className="hover:text-white cursor-pointer">Chat</p>
          <p className="hover:text-white cursor-pointer">Summary</p>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-6 overflow-y-auto">
        {children}
      </main>
    </div>
  );
}
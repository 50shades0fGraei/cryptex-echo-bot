export default function CryptexDashboard() {
  return (
    <div className="bg-space text-platinum min-h-screen p-6 font-sans">
      <main className="flex flex-col gap-8">
        <h1 className="text-4xl font-bold text-neon mb-4">Cryptex Echo Bot</h1>

        <p className="text-electric text-lg">
          The cockpit is live. Trade flow coming soon...
        </p>

        <ol className="font-mono list-inside list-decimal text-platinum">
          <li className="mb-2 tracking-tight">
            Get started by editing{' '}
            <code className="bg-black/5 px-1 rounded">src/pages/index.tsx</code>.
          </li>
          <li className="tracking-tight">
            Save and see your changes instantly.
          </li>
        </ol>

        <div className="flex gap-4 items-center">
          <a
            className="rounded-full border border-neon px-4 py-2 text-neon hover:bg-neon hover:text-space transition"
            href="https://vercel.com/new?utm_source=cryptex"
            target="_blank"
            rel="noopener noreferrer"
          >
            Deploy Cryptex Echo Bot
          </a>
        </div>
      </main>
    </div>
  )
}


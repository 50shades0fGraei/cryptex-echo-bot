import { useState, FormEvent } from 'react';
import Link from 'next/link';

export default function SettingsPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isError, setIsError] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setMessage('');
    setIsError(false);

    try {
      const response = await fetch('http://localhost:5001/api/credentials', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'An unknown error occurred.');
      }

      setMessage(data.message);
    } catch (error: any) {
      setMessage(error.message);
      setIsError(true);
    }
  };

  return (
    <main className="font-sans bg-gray-900 text-gray-200 min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-cyan-400">⚙️ Account Settings</h1>
          <p className="text-gray-400 mt-2">Enter your Webull credentials to connect your account.</p>
        </header>

        <section className="bg-gray-800 p-6 rounded-lg shadow-lg max-w-md mx-auto">
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Webull Email"
              required
              className="bg-gray-700 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
            />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Webull Password"
              required
              className="bg-gray-700 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
            />
            <button type="submit" className="bg-cyan-600 hover:bg-cyan-700 text-white font-bold py-2 px-4 rounded-md">
              Save Credentials
            </button>
          </form>
          {message && (
            <p className={`mt-4 text-center ${isError ? 'text-red-400' : 'text-green-400'}`}>
              {message}
            </p>
          )}
        </section>
        <div className="text-center mt-8">
            <Link href="/" className="text-cyan-400 hover:text-cyan-300">&larr; Back to Dashboard</Link>
        </div>
      </div>
    </main>
  );
}
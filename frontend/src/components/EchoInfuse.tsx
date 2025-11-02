export default function EchoInfuse() {
  return (
    <div className="mb-6">
      <h2 className="text-xl text-neon mb-2">Infuse Capital</h2>
      <input
        type="number"
        placeholder="Enter amount"
        className="bg-graphite text-platinum p-2 rounded w-full"
      />
      <button className="mt-2 px-4 py-2 bg-neon text-space rounded hover:bg-electric transition">
        Infuse
      </button>
    </div>
  )
}

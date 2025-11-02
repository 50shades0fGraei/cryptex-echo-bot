import EchoBottomDollar from '@/components/EchoBottomDollar'
import EchoTradeFlow from '@/components/EchoTradeFlow'
import EchoInfuse from '@/components/EchoInfuse'

export default function CryptexDashboard() {
  return (
    <div className="bg-space text-platinum min-h-screen p-6">
      <h1 className="text-3xl font-bold text-neon mb-4">Cryptex Echo Bot</h1>
      <EchoBottomDollar />
      <EchoTradeFlow />
      <EchoInfuse />
    </div>
  )
}

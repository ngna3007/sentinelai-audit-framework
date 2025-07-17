import React from 'react'
import EvidenceTracker from '../components/EvidenceTracker'

const DashboardHome = () => {
  return (
    <main className='w-full flex flex-col items-center justify-center relative overflow-x-hidden'>
      <div className="w-full">
        <EvidenceTracker/>
      </div>
    </main>
  )
}

export default DashboardHome

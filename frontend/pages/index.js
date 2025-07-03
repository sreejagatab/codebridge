import { useState, useEffect } from 'react'

export default function Home() {
  const [backendStatus, setBackendStatus] = useState('Checking...')
  const [healthData, setHealthData] = useState(null)

  useEffect(() => {
    // Check backend connection
    fetch('http://localhost:3047/api/health')
      .then(response => response.json())
      .then(data => {
        setBackendStatus('Connected ✅')
        setHealthData(data)
      })
      .catch(() => {
        setBackendStatus('Disconnected ❌')
      })
  }, [])

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-blue-600 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"></div>
        <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
          <div className="max-w-md mx-auto">
            <div className="text-center">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                🌉 CodeBridge
              </h1>
              <p className="text-lg text-gray-600 mb-8">
                Bridging the Gap Between Code and Community
              </p>
            </div>
            
            <div className="divide-y divide-gray-200">
              <div className="py-4 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                <div className="flex items-center justify-between">
                  <span>Backend Status:</span>
                  <span className="font-semibold">{backendStatus}</span>
                </div>
                
                {healthData && (
                  <>
                    <div className="flex items-center justify-between">
                      <span>App Version:</span>
                      <span className="font-semibold">{healthData.version}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Environment:</span>
                      <span className="font-semibold">{healthData.environment}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>System:</span>
                      <span className="font-semibold">{healthData.system?.platform}</span>
                    </div>
                  </>
                )}
              </div>
              
              <div className="pt-6 text-base leading-6 font-bold sm:text-lg sm:leading-7">
                <div className="space-y-2">
                  <a href="http://localhost:3047/docs" 
                     target="_blank" 
                     rel="noopener noreferrer"
                     className="block w-full text-center px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors">
                    📖 API Documentation
                  </a>
                  <a href="http://localhost:3047/api/health" 
                     target="_blank" 
                     rel="noopener noreferrer"
                     className="block w-full text-center px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors">
                    🏥 Health Check
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

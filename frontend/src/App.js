import React, { useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ImageUpload from './components/ImageUpload';
import DetectionResults from './components/DetectionResults';
import ModelInfo from './components/ModelInfo';
import { Waves } from 'lucide-react';

function App() {
  const [detectionResults, setDetectionResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [settings, setSettings] = useState({
    conf_threshold: 0.4,
    iou_threshold: 0.45
  });

  const handleDetectionComplete = (results) => {
    setDetectionResults(results);
    setLoading(false);
    setError(null);
  };

  const handleDetectionError = (errorMessage) => {
    setError(errorMessage);
    setLoading(false);
  };

  const handleSettingsChange = (newSettings) => {
    setSettings(newSettings);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <Header />
      <div className="flex">
        <Sidebar 
          settings={settings}
          onSettingsChange={handleSettingsChange}
        />
        <main className="flex-1 p-8">
          <div className="max-w-7xl mx-auto">

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <ImageUpload
                  onDetectionComplete={handleDetectionComplete}
                  onDetectionError={handleDetectionError}
                  setLoading={setLoading}
                  settings={settings}
                />
                
                {loading && (
                  <div className="mt-6 bg-white rounded-lg shadow-md p-8 text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-600">Analyzing image...</p>
                  </div>
                )}

                {error && (
                  <div className="mt-6 bg-red-50 border border-red-200 rounded-lg p-4">
                    <p className="text-red-600">{error}</p>
                  </div>
                )}

                {detectionResults && !loading && (
                  <DetectionResults results={detectionResults} />
                )}
              </div>

              <div className="lg:col-span-1">
                <ModelInfo />
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;

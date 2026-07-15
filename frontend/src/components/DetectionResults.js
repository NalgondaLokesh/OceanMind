import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { AlertCircle, CheckCircle, TrendingUp } from 'lucide-react';

function DetectionResults({ results }) {
  const severityColors = {
    'Low': 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
    'Medium': 'bg-yellow-500/20 text-yellow-300 border-yellow-500/40',
    'High': 'bg-orange-500/20 text-orange-300 border-orange-500/40',
    'Critical': 'bg-red-500/20 text-red-300 border-red-500/40'
  };

  const severityIcons = {
    'Low': <CheckCircle className="w-5 h-5 text-emerald-400" />,
    'Medium': <AlertCircle className="w-5 h-5 text-yellow-400" />,
    'High': <AlertCircle className="w-5 h-5 text-orange-400" />,
    'Critical': <AlertCircle className="w-5 h-5 text-red-400" />
  };

  const detections = results.detections || [];
  const classCounts = results.class_counts || {};
  
  const chartData = Object.entries(classCounts).map(([name, count]) => ({
    name,
    count
  }));

  console.log('DetectionResults - annotated_image:', results.annotated_image ? 'present' : 'missing');
  console.log('DetectionResults - detections:', detections);

  return (
    <div className="space-y-6">
      <div className="bg-slate-800/50 backdrop-blur-lg rounded-lg border border-slate-700 p-6">
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp className="w-5 h-5 text-cyan-400" />
          <h2 className="text-xl font-semibold text-white">Detection Results</h2>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-gradient-to-br from-cyan-500 to-blue-600 rounded-lg p-4 text-white">
            <div className="text-3xl font-bold">{results.total_items || 0}</div>
            <div className="text-sm opacity-80">Total Items</div>
          </div>
          
          <div className={`rounded-lg p-4 border-2 ${severityColors[results.severity] || 'bg-slate-700 text-slate-300 border-slate-600'}`}>
            <div className="flex items-center gap-2 mb-1">
              {severityIcons[results.severity] || <CheckCircle className="w-5 h-5 text-slate-400" />}
              <div className="text-2xl font-bold">{results.severity || 'Unknown'}</div>
            </div>
            <div className="text-sm opacity-80">Severity</div>
          </div>
          
          <div className="bg-slate-700/50 rounded-lg p-4 border border-slate-600">
            <div className="text-3xl font-bold text-cyan-400">{Object.keys(classCounts).length}</div>
            <div className="text-sm text-slate-300">Debris Types</div>
          </div>
          
          <div className="bg-slate-700/50 rounded-lg p-4 border border-slate-600">
            <div className="text-3xl font-bold text-cyan-400">
              {detections.length > 0 
                ? (detections.reduce((sum, d) => sum + d.confidence, 0) / detections.length * 100).toFixed(1)
                : 0}%
            </div>
            <div className="text-sm text-slate-300">Avg Confidence</div>
          </div>
        </div>

        {results.annotated_image && (
          <div className="mb-6">
            <h3 className="text-lg font-medium text-white mb-3">Annotated Image</h3>
            <img
              src={`data:image/jpeg;base64,${results.annotated_image}`}
              alt="Annotated detection"
              className="w-full rounded-lg border border-slate-600 max-h-96 object-contain"
              onError={(e) => console.error('Image load error:', e)}
            />
          </div>
        )}
      </div>

      {detections.length > 0 && (
        <div className="bg-slate-800/50 backdrop-blur-lg rounded-lg border border-slate-700 p-6">
          <h3 className="text-lg font-medium text-white mb-4">Detections</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-600">
                  <th className="text-left py-2 px-3 text-slate-300 font-medium">Class</th>
                  <th className="text-left py-2 px-3 text-slate-300 font-medium">Confidence</th>
                  <th className="text-left py-2 px-3 text-slate-300 font-medium">Bounding Box</th>
                </tr>
              </thead>
              <tbody>
                {detections.map((detection, index) => (
                  <tr key={index} className="border-b border-slate-700 hover:bg-slate-700/50">
                    <td className="py-2 px-3 text-slate-200">{detection.class_name}</td>
                    <td className="py-2 px-3 text-slate-200">{(detection.confidence * 100).toFixed(1)}%</td>
                    <td className="py-2 px-3 text-sm text-slate-400">
                      [{detection.bbox.x1.toFixed(0)}, {detection.bbox.y1.toFixed(0)}, {detection.bbox.x2.toFixed(0)}, {detection.bbox.y2.toFixed(0)}]
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {chartData.length > 0 && (
        <div className="bg-slate-800/50 backdrop-blur-lg rounded-lg border border-slate-700 p-6">
          <h3 className="text-lg font-medium text-white mb-4">Class Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
              <XAxis dataKey="name" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569', borderRadius: '8px' }}
                itemStyle={{ color: '#e2e8f0' }}
              />
              <Bar dataKey="count" fill="#06b6d4" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

export default DetectionResults;

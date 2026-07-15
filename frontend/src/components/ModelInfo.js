import React, { useState, useEffect } from 'react';
import { Cpu, Zap, Target, Layers } from 'lucide-react';
import axios from 'axios';

function ModelInfo() {
  const [modelInfo, setModelInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchModelInfo();
  }, []);

  const fetchModelInfo = async () => {
    try {
      const response = await axios.get('http://localhost:8000/model-info');
      setModelInfo(response.data);
    } catch (error) {
      console.error('Failed to fetch model info:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          <div className="h-4 bg-gray-200 rounded w-2/3"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-slate-800/50 backdrop-blur-lg rounded-lg border border-slate-700 p-6">
      <h2 className="text-xl font-semibold text-white mb-6">Model Information</h2>
      
      {modelInfo && (
        <div className="space-y-4">
          <div className="flex items-start gap-3">
            <Cpu className="w-5 h-5 text-cyan-400 mt-1" />
            <div>
              <div className="font-medium text-white">Model</div>
              <div className="text-sm text-slate-300">{modelInfo.model}</div>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <Target className="w-5 h-5 text-emerald-400 mt-1" />
            <div>
              <div className="font-medium text-white">mAP50</div>
              <div className="text-sm text-slate-300">{modelInfo.mAP50}</div>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <Zap className="w-5 h-5 text-yellow-400 mt-1" />
            <div>
              <div className="font-medium text-white">Precision</div>
              <div className="text-sm text-slate-300">{modelInfo.precision}</div>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <Layers className="w-5 h-5 text-purple-400 mt-1" />
            <div>
              <div className="font-medium text-white">Classes</div>
              <div className="text-sm text-slate-300">{modelInfo.num_classes} debris types</div>
            </div>
          </div>

          <div className="border-t border-slate-700 pt-4 mt-4">
            <div className="font-medium text-white mb-2">Class Names</div>
            <div className="flex flex-wrap gap-2">
              {modelInfo.class_names && typeof modelInfo.class_names === 'object' 
                ? Object.values(modelInfo.class_names).map((name, index) => (
                    <span
                      key={index}
                      className="bg-cyan-500/20 text-cyan-300 px-2 py-1 rounded text-xs border border-cyan-500/30"
                    >
                      {name}
                    </span>
                  ))
                : Array.isArray(modelInfo.class_names)
                ? modelInfo.class_names.map((name, index) => (
                    <span
                      key={index}
                      className="bg-cyan-500/20 text-cyan-300 px-2 py-1 rounded text-xs border border-cyan-500/30"
                    >
                      {name}
                    </span>
                  ))
                : <span className="text-slate-500 text-sm">No class names available</span>
              }
            </div>
          </div>

          <div className="border-t border-slate-700 pt-4 mt-4 space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Confidence Threshold</span>
              <span className="font-medium text-white">{modelInfo.conf_threshold.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">IoU Threshold</span>
              <span className="font-medium text-white">{modelInfo.iou_threshold.toFixed(2)}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ModelInfo;

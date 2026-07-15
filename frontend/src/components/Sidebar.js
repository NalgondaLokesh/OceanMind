import React from 'react';
import { Settings, BarChart3, Info } from 'lucide-react';

function Sidebar({ settings, onSettingsChange }) {
  return (
    <aside className="w-64 bg-slate-800/50 backdrop-blur-lg border-r border-slate-700 p-6 min-h-screen">
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-4">
          <Settings className="w-5 h-5 text-cyan-400" />
          <h2 className="text-lg font-semibold text-white">Settings</h2>
        </div>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-blue-200 mb-2">
              Confidence Threshold: {settings.conf_threshold.toFixed(2)}
            </label>
            <input
              type="range"
              min="0.1"
              max="0.9"
              step="0.05"
              value={settings.conf_threshold}
              onChange={(e) => onSettingsChange({
                ...settings,
                conf_threshold: parseFloat(e.target.value)
              })}
              className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-cyan-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-blue-200 mb-2">
              IoU Threshold: {settings.iou_threshold.toFixed(2)}
            </label>
            <input
              type="range"
              min="0.1"
              max="0.9"
              step="0.05"
              value={settings.iou_threshold}
              onChange={(e) => onSettingsChange({
                ...settings,
                iou_threshold: parseFloat(e.target.value)
              })}
              className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-cyan-500"
            />
          </div>
        </div>
      </div>

      <div className="border-t border-slate-700 pt-6">
        <div className="flex items-center gap-2 mb-4">
          <BarChart3 className="w-5 h-5 text-cyan-400" />
          <h2 className="text-lg font-semibold text-white">Performance</h2>
        </div>
        
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-gradient-to-br from-cyan-500 to-blue-600 rounded-lg p-3 text-white text-center">
            <div className="text-2xl font-bold">70.8%</div>
            <div className="text-xs opacity-80">mAP50</div>
          </div>
          <div className="bg-gradient-to-br from-teal-500 to-emerald-600 rounded-lg p-3 text-white text-center">
            <div className="text-2xl font-bold">81.9%</div>
            <div className="text-xs opacity-80">Precision</div>
          </div>
        </div>
      </div>

      <div className="border-t border-slate-700 pt-6 mt-6">
        <div className="flex items-center gap-2 mb-4">
          <Info className="w-5 h-5 text-cyan-400" />
          <h2 className="text-lg font-semibold text-white">Quick Info</h2>
        </div>
        
        <div className="bg-slate-700/50 rounded-lg p-4 text-sm text-blue-200 border border-slate-600">
          <p className="font-medium mb-2">Model: YOLO11s (Fine-tuned)</p>
          <p className="font-medium mb-2">Classes: 6 marine debris types</p>
          <p className="text-xs text-blue-300">Upload images to detect marine debris and assess pollution severity.</p>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;

import React from 'react';
import { Waves } from 'lucide-react';

function Header() {
  return (
    <header className="bg-slate-800/50 backdrop-blur-lg border-b border-slate-700">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-center">
        <div className="flex flex-col items-center gap-2">
          <div className="flex items-center gap-3">
            <Waves className="w-8 h-8 text-cyan-400" />
            <h1 className="text-2xl font-bold text-white">OceanMind</h1>
          </div>
          <p className="text-sm text-blue-300">AI-Powered Marine Debris Detection & Environmental Intelligence</p>
        </div>
      </div>
    </header>
  );
}

export default Header;

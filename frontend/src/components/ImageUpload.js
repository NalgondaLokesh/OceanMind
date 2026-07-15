import React, { useState } from 'react';
import { Upload, Image as ImageIcon } from 'lucide-react';
import axios from 'axios';

function ImageUpload({ onDetectionComplete, onDetectionError, setLoading, settings }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDetect = async () => {
    if (!selectedFile) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('return_image', 'true');

    try {
      // First update settings
      try {
        await axios.post('http://localhost:8000/settings', settings);
      } catch (settingsError) {
        console.warn('Settings update failed:', settingsError);
        // Continue with detection even if settings fail
      }
      
      // Then detect
      const response = await axios.post('http://localhost:8000/detect', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Detection response:', response.data);
      onDetectionComplete(response.data);
    } catch (error) {
      console.error('Detection error:', error);
      console.error('Error response:', error.response?.data);
      onDetectionError(error.response?.data?.detail || error.message || 'Detection failed. Please try again.');
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreview(null);
  };

  return (
    <div className="bg-slate-800/50 backdrop-blur-lg rounded-lg border border-slate-700 p-6">
      <div className="flex items-center gap-2 mb-4">
        <Upload className="w-5 h-5 text-cyan-400" />
        <h2 className="text-xl font-semibold text-white">Upload Image</h2>
      </div>

      {!preview ? (
        <div className="border-2 border-dashed border-slate-600 rounded-lg p-8 text-center hover:border-cyan-500 transition-colors">
          <ImageIcon className="w-12 h-12 text-slate-500 mx-auto mb-4" />
          <p className="text-slate-300 mb-4">Drag and drop an image here, or click to select</p>
          <input
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            className="hidden"
            id="file-upload"
          />
          <label
            htmlFor="file-upload"
            className="inline-block bg-cyan-500 text-white px-6 py-2 rounded-lg cursor-pointer hover:bg-cyan-600 transition-colors"
          >
            Choose Image
          </label>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="relative">
            <img
              src={preview}
              alt="Preview"
              className="w-full rounded-lg max-h-96 object-contain"
            />
            <button
              onClick={handleReset}
              className="absolute top-2 right-2 bg-red-500 text-white p-2 rounded-full hover:bg-red-600 transition-colors"
            >
              ×
            </button>
          </div>
          
          <div className="flex gap-3">
            <button
              onClick={handleDetect}
              className="flex-1 bg-cyan-500 text-white px-6 py-3 rounded-lg hover:bg-cyan-600 transition-colors font-medium"
            >
              Detect Debris
            </button>
            <button
              onClick={handleReset}
              className="px-6 py-3 border border-slate-600 text-slate-300 rounded-lg hover:bg-slate-700 transition-colors"
            >
              Reset
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default ImageUpload;

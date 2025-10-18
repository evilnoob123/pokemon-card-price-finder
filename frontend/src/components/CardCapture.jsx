import React, { useState, useRef } from 'react';

const CardCapture = ({ onImageCapture, isLoading }) => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [error, setError] = useState(null);
  
  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);

  const handleFileUpload = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.type.startsWith('image/')) {
        setSelectedImage(file);
        setPreviewUrl(URL.createObjectURL(file));
        setError(null);
      } else {
        setError('Please select a valid image file');
      }
    }
  };

  const openCamera = async () => {
    try {
      // Check if getUserMedia is supported
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('Camera not supported on this device');
      }

      // Request camera permissions with mobile-optimized settings
      const constraints = {
        video: {
          facingMode: { ideal: 'environment' }, // Use back camera
          width: { ideal: 1920, min: 640 },
          height: { ideal: 1080, min: 480 },
          aspectRatio: { ideal: 16/9 }
        },
        audio: false
      };

      // Try to get user media
      const mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
      
      setStream(mediaStream);
      setIsCameraOpen(true);
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        
        // Wait for video to be ready
        videoRef.current.onloadedmetadata = () => {
          videoRef.current.play().catch(err => {
            console.warn('Video autoplay failed:', err);
          });
        };
      }
    } catch (err) {
      console.error('Error accessing camera:', err);
      
      // Provide specific error messages for different scenarios
      if (err.name === 'NotAllowedError') {
        setError('Camera access denied. Please allow camera permissions and try again.');
      } else if (err.name === 'NotFoundError') {
        setError('No camera found on this device.');
      } else if (err.name === 'NotSupportedError') {
        setError('Camera not supported on this device.');
      } else if (err.name === 'NotReadableError') {
        setError('Camera is being used by another application.');
      } else {
        setError('Unable to access camera. Please check permissions and try again.');
      }
    }
  };

  const closeCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    setIsCameraOpen(false);
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      const context = canvas.getContext('2d');
      
      if (context) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0);
        
        canvas.toBlob((blob) => {
          if (blob) {
            const file = new File([blob], 'pokemon-card.jpg', { type: 'image/jpeg' });
            setSelectedImage(file);
            setPreviewUrl(URL.createObjectURL(blob));
            setError(null);
            closeCamera();
          }
        }, 'image/jpeg', 0.8);
      }
    }
  };

  const sendToAPI = async () => {
    if (!selectedImage) return;

    try {
      await onImageCapture(selectedImage);
    } catch (err) {
      setError('Failed to process image');
    }
  };

  const clearImage = () => {
    setSelectedImage(null);
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
      setPreviewUrl(null);
    }
    setError(null);
  };

  return (
    <div className="w-full max-w-md mx-auto p-6 bg-white rounded-xl shadow-lg">
      <h2 className="text-2xl font-bold text-center mb-6 text-gray-800">
        📸 Capture Pokémon Card
      </h2>

      {/* Image Preview */}
      {previewUrl && (
        <div className="mb-6">
          <div className="relative">
            <img
              src={previewUrl}
              alt="Pokémon card preview"
              className="w-full h-64 object-contain rounded-lg border-2 border-gray-200 bg-gray-50"
            />
            <button
              onClick={clearImage}
              className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center hover:bg-red-600 transition-colors"
              aria-label="Remove image"
            >
              ×
            </button>
          </div>
        </div>
      )}

      {/* Camera View */}
      {isCameraOpen && (
        <div className="mb-6 relative">
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="w-full h-64 object-cover rounded-lg"
            style={{ transform: 'scaleX(-1)' }} // Mirror the video for better UX
          />
          <canvas ref={canvasRef} className="hidden" />
          
          {/* Camera overlay with instructions */}
          <div className="absolute top-2 left-2 right-2 bg-black bg-opacity-50 text-white text-xs p-2 rounded">
            📱 Position your Pokémon card in the frame
          </div>
          
          <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex gap-4">
            <button
              onClick={capturePhoto}
              className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors font-medium shadow-lg"
            >
              📷 Capture
            </button>
            <button
              onClick={closeCamera}
              className="bg-gray-500 text-white px-6 py-3 rounded-lg hover:bg-gray-600 transition-colors font-medium shadow-lg"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      {!isCameraOpen && (
        <div className="space-y-3">
          <button
            onClick={() => fileInputRef.current?.click()}
            className="w-full bg-green-500 text-white py-3 px-4 rounded-lg hover:bg-green-600 transition-colors font-medium flex items-center justify-center gap-2"
          >
            📁 Upload Image
          </button>
          
          {/* Check if camera is supported before showing camera button */}
          {navigator.mediaDevices && navigator.mediaDevices.getUserMedia ? (
            <button
              onClick={openCamera}
              className="w-full bg-blue-500 text-white py-3 px-4 rounded-lg hover:bg-blue-600 transition-colors font-medium flex items-center justify-center gap-2"
            >
              📷 Take Photo
            </button>
          ) : (
            <div className="w-full bg-gray-300 text-gray-600 py-3 px-4 rounded-lg text-center text-sm">
              📷 Camera not supported on this device
            </div>
          )}
        </div>
      )}

      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileUpload}
        className="hidden"
      />

      {/* Scan Button */}
      {selectedImage && !isCameraOpen && (
        <button
          onClick={sendToAPI}
          disabled={isLoading}
          className="w-full mt-4 bg-purple-500 text-white py-3 px-4 rounded-lg hover:bg-purple-600 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {isLoading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              Scanning...
            </>
          ) : (
            '🔍 Scan Card'
          )}
        </button>
      )}

      {/* Error Message */}
      {error && (
        <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {/* Instructions */}
      <div className="mt-6 text-sm text-gray-600 text-center">
        <p className="mb-2">📱 Upload an image or take a photo of your Pokémon card</p>
        <p className="text-xs mb-2">Make sure the card is well-lit and clearly visible</p>
        <div className="text-xs text-gray-500 bg-gray-50 p-2 rounded">
          <p className="font-semibold mb-1">📱 Mobile Camera Tips:</p>
          <ul className="text-left space-y-1">
            <li>• Allow camera permissions when prompted</li>
            <li>• Use the back camera for better quality</li>
            <li>• Ensure good lighting</li>
            <li>• Hold phone steady</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default CardCapture;
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

      // Request camera permissions with portrait orientation
      const constraints = {
        video: {
          facingMode: 'environment', // Use back camera
          width: { ideal: 720 },   // Portrait: height > width
          height: { ideal: 1280 },
          aspectRatio: { ideal: 9/16 } // Portrait aspect ratio
        },
        audio: false
      };

      console.log('Requesting camera access...');
      
      // Try to get user media
      const mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
      
      console.log('Camera access granted, setting up video...');
      
      setStream(mediaStream);
      setIsCameraOpen(true);
      
      // Wait for the next tick to ensure the video element is rendered
      setTimeout(() => {
        if (videoRef.current) {
          console.log('Setting video source...');
          videoRef.current.srcObject = mediaStream;
          
          // Wait for video to be ready
          videoRef.current.onloadedmetadata = () => {
            console.log('Video metadata loaded, starting playback...');
            videoRef.current.play().catch(err => {
              console.warn('Video autoplay failed:', err);
              // Try to play again after user interaction
              setTimeout(() => {
                videoRef.current.play().catch(console.warn);
              }, 100);
            });
          };
          
          videoRef.current.oncanplay = () => {
            console.log('Video can play');
          };
          
          videoRef.current.onerror = (e) => {
            console.error('Video error:', e);
            setError('Video playback failed. Please try again.');
          };
        }
      }, 100);
      
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
        setError(`Unable to access camera: ${err.message}`);
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
    console.log('Attempting to capture photo...');
    
    if (!videoRef.current || !canvasRef.current) {
      console.error('Video or canvas ref not available');
      setError('Camera not ready. Please try again.');
      return;
    }

    const canvas = canvasRef.current;
    const video = videoRef.current;
    
    if (!video.videoWidth || !video.videoHeight) {
      console.error('Video dimensions not available');
      setError('Video not ready. Please wait and try again.');
      return;
    }

    console.log(`Video dimensions: ${video.videoWidth}x${video.videoHeight}`);
    
    const context = canvas.getContext('2d');
    
    if (!context) {
      console.error('Could not get canvas context');
      setError('Failed to capture image. Please try again.');
      return;
    }
    
    try {
      // Get the video element's display dimensions (what user sees)
      const videoRect = video.getBoundingClientRect();
      const videoDisplayWidth = videoRect.width;
      const videoDisplayHeight = videoRect.height;
      
      // Get the actual video stream dimensions
      const videoStreamWidth = video.videoWidth;
      const videoStreamHeight = video.videoHeight;
      
      console.log(`Video display: ${videoDisplayWidth}x${videoDisplayHeight}`);
      console.log(`Video stream: ${videoStreamWidth}x${videoStreamHeight}`);
      
      // Set canvas to match the display dimensions (what user sees)
      canvas.width = videoDisplayWidth;
      canvas.height = videoDisplayHeight;
      
      // Calculate scaling factors to crop the video stream to match display
      const scaleX = videoStreamWidth / videoDisplayWidth;
      const scaleY = videoStreamHeight / videoDisplayHeight;
      const scale = Math.max(scaleX, scaleY); // Use the larger scale to ensure we crop properly
      
      // Calculate the source rectangle to crop from the video stream
      const sourceWidth = videoDisplayWidth * scale;
      const sourceHeight = videoDisplayHeight * scale;
      const sourceX = (videoStreamWidth - sourceWidth) / 2;
      const sourceY = (videoStreamHeight - sourceHeight) / 2;
      
      console.log(`Capture source: ${sourceX}, ${sourceY}, ${sourceWidth}, ${sourceHeight}`);
      
      // Draw the cropped video frame to canvas (exactly what user sees)
      context.drawImage(
        video,
        sourceX, sourceY, sourceWidth, sourceHeight, // Source rectangle
        0, 0, canvas.width, canvas.height // Destination rectangle
      );
      
      console.log('Image drawn to canvas, converting to blob...');
      
      // Convert canvas to blob
      canvas.toBlob((blob) => {
        if (blob) {
          console.log('Blob created successfully, size:', blob.size);
          
          // Create file from blob
          const file = new File([blob], 'pokemon-card.jpg', { type: 'image/jpeg' });
          
          // Set the captured image
          setSelectedImage(file);
          setPreviewUrl(URL.createObjectURL(blob));
          setError(null);
          
          console.log('Photo captured successfully');
          
          // Close camera
          closeCamera();
        } else {
          console.error('Failed to create blob from canvas');
          setError('Failed to capture image. Please try again.');
        }
      }, 'image/jpeg', 0.9); // Higher quality for better results
      
    } catch (err) {
      console.error('Error during photo capture:', err);
      setError('Failed to capture image. Please try again.');
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
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="text-center mb-6">
        <h2 className="text-xl font-bold text-gray-900 mb-2">
          📸 Capture Pokémon Card
        </h2>
        <p className="text-sm text-gray-600">
          Upload an image or take a photo to get started
        </p>
      </div>

      {/* Image Preview */}
      {previewUrl && (
        <div className="mb-6">
          <div className="relative">
            <img
              src={previewUrl}
              alt="Pokémon card preview"
              className="w-full h-64 object-contain rounded-lg border border-gray-200 bg-gray-50"
            />
            <button
              onClick={clearImage}
              className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center hover:bg-red-600 transition-colors text-sm"
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
            className="w-full h-64 object-cover rounded-lg bg-gray-900"
            style={{ transform: 'scaleX(-1)' }} // Mirror the video for better UX
          />
          <canvas ref={canvasRef} className="hidden" />
          
          {/* Camera overlay with instructions */}
          <div className="absolute top-2 left-2 right-2 bg-black bg-opacity-50 text-white text-xs p-2 rounded">
            📱 Position your Pokémon card in the frame
          </div>
          
          {/* Loading indicator */}
          {!stream && (
            <div className="absolute inset-0 flex items-center justify-center bg-gray-900 rounded-lg">
              <div className="text-white text-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto mb-2"></div>
                <p className="text-sm">Starting camera...</p>
              </div>
            </div>
          )}
          
          <div className="absolute bottom-2 left-1/2 transform -translate-x-1/2 flex gap-2">
            <button
              onClick={capturePhoto}
              disabled={!stream}
              className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors font-medium text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              📷 Capture
            </button>
            <button
              onClick={closeCamera}
              className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600 transition-colors font-medium text-sm"
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
            className="w-full bg-gradient-to-r from-green-500 to-green-600 text-white py-3 px-4 rounded-lg hover:from-green-600 hover:to-green-700 transition-all font-medium flex items-center justify-center gap-2 shadow-sm"
          >
            📁 Upload Image
          </button>
          
          {/* Check if camera is supported before showing camera button */}
          {navigator.mediaDevices && navigator.mediaDevices.getUserMedia ? (
            <button
              onClick={openCamera}
              className="w-full bg-gradient-to-r from-blue-500 to-blue-600 text-white py-3 px-4 rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all font-medium flex items-center justify-center gap-2 shadow-sm"
            >
              📷 Take Photo
            </button>
          ) : (
            <div className="w-full bg-gray-100 text-gray-500 py-3 px-4 rounded-lg text-center text-sm">
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
          className="w-full mt-4 bg-gradient-to-r from-purple-500 to-purple-600 text-white py-3 px-4 rounded-lg hover:from-purple-600 hover:to-purple-700 transition-all font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-sm"
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
        <div className="mt-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
          {error}
        </div>
      )}

      {/* Instructions */}
      <div className="mt-6 text-xs text-gray-500">
        <div className="bg-gray-50 p-3 rounded-lg">
          <p className="font-semibold mb-2 text-gray-700">📱 Mobile Camera Tips:</p>
          <ul className="space-y-1 text-left">
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
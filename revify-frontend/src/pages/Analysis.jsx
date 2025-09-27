import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  MagnifyingGlassIcon,
  ChartBarIcon,
  DocumentTextIcon,
  SparklesIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline';
import { revifyAPI } from '../services/api';

const Analysis = () => {
  const [status, setStatus] = useState({
    is_running: false,
    progress: 0,
    current_phase: '',
    error: null,
    result: null,
    start_time: null
  });
  const [elapsedTime, setElapsedTime] = useState(0);
  
  const location = useLocation();
  const navigate = useNavigate();
  
  const productUrl = location.state?.productUrl || '';
  const productName = location.state?.productName || 'Product Analysis';

  useEffect(() => {
    if (!productUrl) {
      navigate('/');
      return;
    }

    // Start polling for status updates
    const pollStatus = async () => {
      try {
        const statusData = await revifyAPI.getAnalysisStatus();
        setStatus(statusData);

        // Calculate elapsed time if analysis is running
        if (statusData.start_time) {
          const startTime = new Date(statusData.start_time);
          const now = new Date();
          const elapsed = Math.floor((now - startTime) / 1000);
          setElapsedTime(elapsed);
        }

        // If analysis is complete, navigate to results
        if (statusData.result && !statusData.is_running && !statusData.error) {
          setTimeout(() => {
            navigate('/results', { 
              state: { 
                result: statusData.result,
                productUrl,
                productName
              } 
            });
          }, 2000); // Give user time to see completion
        }
      } catch (error) {
        console.error('Error polling status:', error);
        setStatus(prev => ({
          ...prev,
          error: 'Failed to get analysis status',
          is_running: false
        }));
      }
    };

    // Poll immediately and then every 2 seconds
    pollStatus();
    const interval = setInterval(pollStatus, 2000);

    return () => clearInterval(interval);
  }, [productUrl, navigate]);

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const getPhaseIcon = (phase) => {
    if (phase.toLowerCase().includes('feature')) {
      return MagnifyingGlassIcon;
    } else if (phase.toLowerCase().includes('review') || phase.toLowerCase().includes('scrap')) {
      return DocumentTextIcon;
    } else if (phase.toLowerCase().includes('analyz')) {
      return ChartBarIcon;
    } else {
      return SparklesIcon;
    }
  };

  const analysisSteps = [
    { 
      id: 'initialize',
      title: 'Initializing',
      description: 'Setting up analysis environment',
      range: [0, 20]
    },
    { 
      id: 'extract',
      title: 'Feature Extraction',
      description: 'Identifying key product features',
      range: [20, 40]
    },
    { 
      id: 'scrape',
      title: 'Review Scraping',
      description: 'Gathering customer reviews',
      range: [40, 70]
    },
    { 
      id: 'analyze',
      title: 'AI Analysis',
      description: 'Processing sentiment and insights',
      range: [70, 95]
    },
    { 
      id: 'complete',
      title: 'Finalizing',
      description: 'Preparing comprehensive report',
      range: [95, 100]
    }
  ];

  const getCurrentStep = () => {
    return analysisSteps.find(step => 
      status.progress >= step.range[0] && status.progress < step.range[1]
    ) || analysisSteps[0];
  };

  const currentStep = getCurrentStep();
  const PhaseIcon = getPhaseIcon(status.current_phase);

  if (status.error) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="max-w-md w-full text-center"
        >
          <div className="bg-white rounded-2xl shadow-xl p-8 border border-red-200">
            <ExclamationTriangleIcon className="h-16 w-16 text-red-500 mx-auto mb-6" />
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Analysis Failed</h2>
            <p className="text-gray-600 mb-6">{status.error}</p>
            <div className="space-y-3">
              <button
                onClick={() => window.location.reload()}
                className="w-full btn-primary flex items-center justify-center space-x-2"
              >
                <ArrowPathIcon className="h-5 w-5" />
                <span>Retry Analysis</span>
              </button>
              <button
                onClick={() => navigate('/')}
                className="w-full btn-secondary"
              >
                Back to Home
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 pt-10">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Analyzing Your{' '}
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Product
            </span>
          </h1>
          <p className="text-xl text-gray-600 mb-6">{productName}</p>
          <div className="inline-flex items-center space-x-2 px-4 py-2 bg-white/80 backdrop-blur-sm rounded-full border border-gray-200">
            <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
            <span className="text-sm font-medium text-gray-700">
              Analysis in Progress • {formatTime(elapsedTime)}
            </span>
          </div>
        </motion.div>

        {/* Progress Card */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-gray-200 p-8 mb-8"
        >
          {/* Current Phase */}
          <div className="text-center mb-8">
            <motion.div
              key={status.current_phase}
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.5 }}
              className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-500 rounded-3xl mb-6 shadow-lg"
            >
              <PhaseIcon className="h-10 w-10 text-white" />
            </motion.div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">{currentStep.title}</h2>
            <p className="text-gray-600">{status.current_phase || currentStep.description}</p>
          </div>

          {/* Progress Bar */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-gray-700">Progress</span>
              <span className="text-sm font-bold text-blue-600">{status.progress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full shadow-sm"
                initial={{ width: 0 }}
                animate={{ width: `${status.progress}%` }}
                transition={{ duration: 0.8, ease: "easeOut" }}
              />
            </div>
          </div>

          {/* Steps */}
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {analysisSteps.map((step, index) => {
              const isCompleted = status.progress > step.range[1];
              const isActive = status.progress >= step.range[0] && status.progress < step.range[1];
              const isPending = status.progress < step.range[0];

              return (
                <motion.div
                  key={step.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className={`text-center p-4 rounded-2xl transition-all duration-300 ${
                    isCompleted
                      ? 'bg-green-50 border border-green-200'
                      : isActive
                      ? 'bg-blue-50 border border-blue-200 ring-2 ring-blue-100'
                      : 'bg-gray-50 border border-gray-200'
                  }`}
                >
                  <div
                    className={`w-8 h-8 rounded-full mx-auto mb-3 flex items-center justify-center text-sm font-bold transition-all duration-300 ${
                      isCompleted
                        ? 'bg-green-500 text-white'
                        : isActive
                        ? 'bg-blue-500 text-white animate-pulse'
                        : 'bg-gray-300 text-gray-600'
                    }`}
                  >
                    {isCompleted ? (
                      <CheckCircleIcon className="h-5 w-5" />
                    ) : (
                      index + 1
                    )}
                  </div>
                  <h3
                    className={`font-semibold text-sm mb-1 ${
                      isCompleted
                        ? 'text-green-800'
                        : isActive
                        ? 'text-blue-800'
                        : 'text-gray-600'
                    }`}
                  >
                    {step.title}
                  </h3>
                  <p
                    className={`text-xs ${
                      isCompleted
                        ? 'text-green-600'
                        : isActive
                        ? 'text-blue-600'
                        : 'text-gray-500'
                    }`}
                  >
                    {step.description}
                  </p>
                </motion.div>
              );
            })}
          </div>
        </motion.div>

        {/* Fun Facts */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white/60 backdrop-blur-sm rounded-2xl p-6 border border-gray-200"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">
            Did You Know? 🤔
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
            <div>
              <div className="text-2xl font-bold text-blue-600 mb-1">95%</div>
              <p className="text-sm text-gray-600">of people read reviews before purchasing</p>
            </div>
            <div>
              <div className="text-2xl font-bold text-purple-600 mb-1">13+</div>
              <p className="text-sm text-gray-600">reviews needed for trust</p>
            </div>
            <div>
              <div className="text-2xl font-bold text-pink-600 mb-1">68%</div>
              <p className="text-sm text-gray-600">trust positive reviews more</p>
            </div>
          </div>
        </motion.div>

        {/* Loading Animation */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="text-center mt-12 mb-8"
        >
          <div className="flex items-center justify-center space-x-2 text-gray-500">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
            <div className="w-2 h-2 bg-pink-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
          </div>
          <p className="mt-4 text-gray-600">
            {status.is_running ? 'Processing your request...' : 'Preparing results...'}
          </p>
        </motion.div>
      </div>
    </div>
  );
};

export default Analysis;
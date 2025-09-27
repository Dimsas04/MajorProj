import React from 'react';
import { motion } from 'framer-motion';

const LoadingSpinner = ({ size = 'medium', message = 'Loading...', color = 'blue' }) => {
  const getSizeClasses = (size) => {
    switch (size) {
      case 'small':
        return 'w-5 h-5 border-2';
      case 'large':
        return 'w-12 h-12 border-4';
      default:
        return 'w-8 h-8 border-3';
    }
  };

  const getColorClasses = (color) => {
    switch (color) {
      case 'white':
        return 'border-white border-t-transparent';
      case 'purple':
        return 'border-purple-500 border-t-transparent';
      case 'green':
        return 'border-green-500 border-t-transparent';
      default:
        return 'border-blue-500 border-t-transparent';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col items-center justify-center space-y-4"
    >
      <div
        className={`${getSizeClasses(size)} ${getColorClasses(color)} rounded-full animate-spin`}
      />
      {message && (
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-gray-600 text-center"
        >
          {message}
        </motion.p>
      )}
    </motion.div>
  );
};

export default LoadingSpinner;
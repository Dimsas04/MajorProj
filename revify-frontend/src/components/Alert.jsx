import React from 'react';
import { motion } from 'framer-motion';
import { ExclamationTriangleIcon, CheckCircleIcon, InformationCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';

const Alert = ({ type = 'info', title, message, onClose, className = '' }) => {
  const getAlertStyles = (type) => {
    switch (type) {
      case 'success':
        return {
          bg: 'bg-green-50 border-green-200',
          text: 'text-green-800',
          icon: CheckCircleIcon,
          iconColor: 'text-green-500'
        };
      case 'warning':
        return {
          bg: 'bg-yellow-50 border-yellow-200',
          text: 'text-yellow-800',
          icon: ExclamationTriangleIcon,
          iconColor: 'text-yellow-500'
        };
      case 'error':
        return {
          bg: 'bg-red-50 border-red-200',
          text: 'text-red-800',
          icon: XCircleIcon,
          iconColor: 'text-red-500'
        };
      default:
        return {
          bg: 'bg-blue-50 border-blue-200',
          text: 'text-blue-800',
          icon: InformationCircleIcon,
          iconColor: 'text-blue-500'
        };
    }
  };

  const styles = getAlertStyles(type);
  const IconComponent = styles.icon;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className={`${styles.bg} border rounded-xl p-4 ${className}`}
    >
      <div className="flex items-start space-x-3">
        <IconComponent className={`h-5 w-5 ${styles.iconColor} flex-shrink-0 mt-0.5`} />
        <div className="flex-1">
          {title && (
            <h4 className={`font-semibold ${styles.text} mb-1`}>{title}</h4>
          )}
          <p className={`${styles.text} text-sm`}>{message}</p>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className={`${styles.text} hover:opacity-70 transition-opacity`}
          >
            <XCircleIcon className="h-5 w-5" />
          </button>
        )}
      </div>
    </motion.div>
  );
};

export default Alert;
import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useStore } from '../store/store';
import { FiTrash2, FiDownload, FiCalendar, FiBarChart2, FiTrendingUp } from 'react-icons/fi';
import { toast } from 'react-toastify';

export const PatientHistory = () => {
  const { user } = useStore();
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedDisease, setSelectedDisease] = useState('all');
  const [sortBy, setSortBy] = useState('recent');

  useEffect(() => {
    loadPredictionHistory();
  }, []);

  const loadPredictionHistory = () => {
    setLoading(true);
    try {
      const userId = user?.id || 'anonymous';
      const history = JSON.parse(localStorage.getItem(`predictionHistory_${userId}`) || '[]');
      setPredictions(history);
    } catch (error) {
      console.error('Error loading history:', error);
      setPredictions([]);
    } finally {
      setLoading(false);
    }
  };

  const deletePrediction = (id) => {
    const updatedPredictions = predictions.filter(p => p.id !== id);
    setPredictions(updatedPredictions);
    const userId = user?.id || 'anonymous';
    localStorage.setItem(`predictionHistory_${userId}`, JSON.stringify(updatedPredictions));
    toast.success('Prediction deleted');
  };

  const deleteAllPredictions = () => {
    if (window.confirm('Are you sure you want to delete all predictions?')) {
      setPredictions([]);
      const userId = user?.id || 'anonymous';
      localStorage.setItem(`predictionHistory_${userId}`, JSON.stringify([]));
      toast.success('All predictions deleted');
    }
  };

  const downloadData = () => {
    const dataStr = JSON.stringify(predictions, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `medical-history-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
    toast.success('Data downloaded successfully');
  };

  const filteredPredictions = predictions.filter(p => 
    selectedDisease === 'all' || p.disease === selectedDisease
  ).sort((a, b) => {
    if (sortBy === 'recent') {
      return new Date(b.timestamp) - new Date(a.timestamp);
    } else if (sortBy === 'risk') {
      return (b.riskScore || 0) - (a.riskScore || 0);
    }
    return 0;
  });

  const getRiskColor = (riskScore) => {
    if (riskScore > 0.7) return 'text-red-400 bg-red-400/10';
    if (riskScore > 0.4) return 'text-yellow-400 bg-yellow-400/10';
    return 'text-green-400 bg-green-400/10';
  };

  const getRiskLabel = (riskScore) => {
    if (riskScore > 0.7) return 'High Risk';
    if (riskScore > 0.4) return 'Medium Risk';
    return 'Low Risk';
  };

  const getDiseaseColor = (disease) => {
    const colors = {
      'dengue': 'from-red-500 to-pink-600',
      'kidney': 'from-cyan-500 to-blue-600',
      'mental_health': 'from-purple-500 to-indigo-600'
    };
    return colors[disease] || 'from-gray-500 to-gray-600';
  };

  const stats = {
    total: predictions.length,
    highRisk: predictions.filter(p => (p.riskScore || 0) > 0.7).length,
    mediumRisk: predictions.filter(p => (p.riskScore || 0) > 0.4 && (p.riskScore || 0) <= 0.7).length,
    lowRisk: predictions.filter(p => (p.riskScore || 0) <= 0.4).length
  };

  return (
    <div className="pt-24 min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-black pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center text-white mb-12"
        >
          <h1 className="text-5xl font-bold mb-4">Medical History</h1>
          <p className="text-xl text-purple-200">Track your health predictions over time</p>
        </motion.div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0 }}
            className="bg-white/10 backdrop-blur-md rounded-lg p-4 border border-white/20"
          >
            <div className="text-3xl font-bold text-white">{stats.total}</div>
            <p className="text-white/60 text-sm">Total Predictions</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-red-500/10 backdrop-blur-md rounded-lg p-4 border border-red-500/30"
          >
            <div className="text-3xl font-bold text-red-400">{stats.highRisk}</div>
            <p className="text-red-200/60 text-sm">High Risk</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-yellow-500/10 backdrop-blur-md rounded-lg p-4 border border-yellow-500/30"
          >
            <div className="text-3xl font-bold text-yellow-400">{stats.mediumRisk}</div>
            <p className="text-yellow-200/60 text-sm">Medium Risk</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-green-500/10 backdrop-blur-md rounded-lg p-4 border border-green-500/30"
          >
            <div className="text-3xl font-bold text-green-400">{stats.lowRisk}</div>
            <p className="text-green-200/60 text-sm">Low Risk</p>
          </motion.div>
        </div>

        <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-white font-semibold mb-2">Disease Type</label>
              <select
                value={selectedDisease}
                onChange={(e) => setSelectedDisease(e.target.value)}
                className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all"
              >
                <option value="all">All Diseases</option>
                <option value="dengue">Dengue</option>
                <option value="kidney">Kidney Disease</option>
                <option value="mental_health">Mental Health</option>
              </select>
            </div>

            <div>
              <label className="block text-white font-semibold mb-2">Sort By</label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all"
              >
                <option value="recent">Most Recent</option>
                <option value="risk">Risk Level</option>
              </select>
            </div>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={downloadData}
              disabled={predictions.length === 0}
              className="py-2 px-4 bg-gradient-to-r from-blue-500 to-cyan-600 text-white font-semibold rounded-lg hover:shadow-lg transition-all disabled:opacity-50 mt-7 flex items-center justify-center gap-2"
            >
              <FiDownload /> Download
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={deleteAllPredictions}
              disabled={predictions.length === 0}
              className="py-2 px-4 bg-gradient-to-r from-red-500 to-pink-600 text-white font-semibold rounded-lg hover:shadow-lg transition-all disabled:opacity-50 mt-7 flex items-center justify-center gap-2"
            >
              <FiTrash2 /> Clear All
            </motion.button>
          </div>
        </div>

        {loading ? (
          <div className="text-center text-white">
            <p className="text-lg">Loading predictions...</p>
          </div>
        ) : filteredPredictions.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="bg-white/10 backdrop-blur-md rounded-xl p-12 border border-white/20 text-center"
          >
            <FiBarChart2 className="mx-auto mb-4 text-white/40" size={48} />
            <p className="text-white text-xl">No predictions found</p>
            <p className="text-white/60 mt-2">Make your first prediction to see it here</p>
          </motion.div>
        ) : (
          <div className="space-y-4">
            {filteredPredictions.map((prediction, idx) => (
              <motion.div
                key={prediction.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.05 }}
                className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20 hover:border-white/40 transition-all"
              >
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
                  <div className="flex-1">
                    <div className="flex items-center gap-4">
                      <div className={`w-16 h-16 rounded-lg bg-gradient-to-br ${getDiseaseColor(prediction.disease)} flex items-center justify-center`}>
                        <FiTrendingUp className="text-white" size={24} />
                      </div>
                      <div>
                        <h3 className="text-xl font-bold text-white capitalize">
                          {prediction.disease.replace('_', ' ')} Prediction
                        </h3>
                        <p className="text-white/60 flex items-center gap-2 mt-1">
                          <FiCalendar size={14} />
                          {new Date(prediction.timestamp).toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'short',
                            day: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-6">
                    <div className="text-center">
                      <div className={`inline-block px-6 py-2 rounded-full font-semibold ${getRiskColor(prediction.riskScore || 0)}`}>
                        {getRiskLabel(prediction.riskScore || 0)}
                      </div>
                      <p className="text-white/60 text-sm mt-2">
                        Score: {((prediction.riskScore || 0) * 100).toFixed(1)}%
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={() => deletePrediction(prediction.id)}
                      className="p-3 bg-red-500/20 border border-red-500/30 rounded-lg text-red-400 hover:bg-red-500/30 transition-all"
                    >
                      <FiTrash2 size={20} />
                    </motion.button>
                  </div>
                </div>

                {prediction.details && (
                  <div className="mt-4 pt-4 border-t border-white/10">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      {Object.entries(prediction.details).slice(0, 4).map(([key, value]) => (
                        <div key={key}>
                          <p className="text-white/60 text-xs capitalize">{key.replace(/_/g, ' ')}</p>
                          <p className="text-white font-semibold">
                            {typeof value === 'number' ? value.toFixed(2) : value}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

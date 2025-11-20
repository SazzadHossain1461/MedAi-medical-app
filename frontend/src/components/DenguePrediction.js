import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { useStore } from '../store/store';
import { dengueAPI } from '../api/api';
import { toast } from 'react-toastify';
import { HeartBeat } from './3D/HeartBeat';

export const DenguePrediction = () => {
  const { t } = useTranslation();
  const { setLoading, loading, setDengueResult, dengueResult } = useStore();

  const [formData, setFormData] = useState({
    age: '',
    temperature: '',
    plateletCount: '',
    whiteBloodCells: '',
    hemoglobin: '',
    hematocrit: '',
    location: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.age || !formData.temperature) {
      toast.error(t('common.error'));
      return;
    }

    setLoading(true);
    try {
      const response = await dengueAPI.predict(formData);
      setDengueResult(response.data);
      toast.success(t('common.success'));
    } catch (error) {
      toast.error('Prediction failed. Please try again.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (risk) => {
    if (risk > 0.7) return 'from-red-500 to-red-600';
    if (risk > 0.4) return 'from-yellow-500 to-orange-600';
    return 'from-green-500 to-emerald-600';
  };

  const getRiskLabel = (risk) => {
    if (risk > 0.7) return t('common.highRisk');
    if (risk > 0.4) return t('common.mediumRisk');
    return t('common.lowRisk');
  };

  return (
    <div className="pt-24 min-h-screen bg-gradient-to-br from-red-400 via-pink-500 to-purple-600 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center text-white mb-12"
        >
          <h1 className="text-5xl font-bold mb-4">{t('dengue.title')}</h1>
          <p className="text-xl text-red-100">{t('dengue.description')}</p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Form */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20"
          >
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-white font-semibold mb-2">
                    {t('dengue.labels.age')}
                  </label>
                  <input
                    type="number"
                    name="age"
                    value={formData.age}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="e.g. 25"
                  />
                </div>
                <div>
                  <label className="block text-white font-semibold mb-2">
                    {t('dengue.labels.temperature')}
                  </label>
                  <input
                    type="number"
                    name="temperature"
                    value={formData.temperature}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="e.g. 38.5"
                    step="0.1"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-white font-semibold mb-2">
                    {t('dengue.labels.plateletCount')}
                  </label>
                  <input
                    type="number"
                    name="plateletCount"
                    value={formData.plateletCount}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="e.g. 150000"
                  />
                </div>
                <div>
                  <label className="block text-white font-semibold mb-2">
                    {t('dengue.labels.whiteBloodCells')}
                  </label>
                  <input
                    type="number"
                    name="whiteBloodCells"
                    value={formData.whiteBloodCells}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="e.g. 5000"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-white font-semibold mb-2">
                    {t('dengue.labels.hemoglobin')}
                  </label>
                  <input
                    type="number"
                    name="hemoglobin"
                    value={formData.hemoglobin}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="e.g. 13.5"
                    step="0.1"
                  />
                </div>
                <div>
                  <label className="block text-white font-semibold mb-2">
                    {t('dengue.labels.hematocrit')}
                  </label>
                  <input
                    type="number"
                    name="hematocrit"
                    value={formData.hematocrit}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="e.g. 40"
                  />
                </div>
              </div>

              <div>
                <label className="block text-white font-semibold mb-2">
                  {t('dengue.labels.location')}
                </label>
                <input
                  type="text"
                  name="location"
                  value={formData.location}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                  placeholder="e.g. Dhaka"
                />
              </div>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-gradient-to-r from-red-500 to-pink-600 text-white font-bold rounded-lg hover:shadow-lg transition-all disabled:opacity-50"
              >
                {loading ? t('common.loading') : t('dengue.predict')}
              </motion.button>
            </form>
          </motion.div>

          {/* 3D Animation & Results */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex flex-col gap-8"
          >
            {/* 3D Animation */}
            <div className="w-full h-80 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 overflow-hidden shadow-2xl">
              <HeartBeat color="#ff4444" />
            </div>

            {/* Results */}
            {dengueResult && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className={`bg-gradient-to-br ${getRiskColor(dengueResult.risk_score)} rounded-2xl p-8 text-white border border-white/20 shadow-2xl`}
              >
                <h3 className="text-2xl font-bold mb-6">{t('dengue.results')}</h3>
                
                <div className="space-y-6">
                  <div>
                    <p className="text-white/80 text-sm mb-2">{t('dengue.riskLevel')}</p>
                    <p className="text-4xl font-bold">{getRiskLabel(dengueResult.risk_score)}</p>
                  </div>

                  <div>
                    <p className="text-white/80 text-sm mb-2">{t('dengue.confidence')}</p>
                    <div className="bg-white/20 rounded-full h-4 mt-2 overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${(dengueResult.confidence || 0.85) * 100}%` }}
                        transition={{ duration: 1, ease: 'easeInOut' }}
                        className="bg-white h-full"
                      />
                    </div>
                    <p className="text-sm mt-3 font-semibold">{((dengueResult.confidence || 0.85) * 100).toFixed(1)}%</p>
                  </div>

                  <div className="pt-6 border-t border-white/30">
                    <p className="font-semibold mb-3">💡 {t('common.recommendation')}</p>
                    <p className="text-white/90 leading-relaxed">
                      {dengueResult.risk_score > 0.7
                        ? t('common.consultDoctor')
                        : t('common.healthyStatus')}
                    </p>
                  </div>
                </div>
              </motion.div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { useStore } from '../store/store';
import { kidneyAPI } from '../api/api';
import { toast } from 'react-toastify';
import { MoleculeAnimation } from './3D/MoleculeAnimation';

export const KidneyPrediction = () => {
  const { t } = useTranslation();
  const { setLoading, loading, setKidneyResult, kidneyResult } = useStore();

  const [formData, setFormData] = useState({
    age: '',
    systolicBP: '',
    diastolicBP: '',
    glucose: '',
    potassium: '',
    creatinine: '',
    bmi: '',
    smokingStatus: 'no'
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
    
    // Validate required fields
    if (!formData.age || !formData.creatinine || !formData.systolicBP || !formData.diastolicBP) {
      toast.error(t('common.error'));
      return;
    }

    // Validate numeric values
    const numFields = ['age', 'systolicBP', 'diastolicBP', 'glucose', 'potassium', 'creatinine', 'bmi'];
    for (const field of numFields) {
      if (formData[field] && isNaN(formData[field])) {
        toast.error(`Invalid ${field}`);
        return;
      }
    }

    setLoading(true);
    try {
      const response = await kidneyAPI.predict(formData);
      setKidneyResult(response.data);
      toast.success(t('common.success'));
    } catch (error) {
      toast.error('Prediction failed. Please try again.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (risk) => {
    if (risk > 0.7) return 'from-blue-600 to-blue-700';
    if (risk > 0.4) return 'from-cyan-500 to-blue-600';
    return 'from-emerald-500 to-teal-600';
  };

  const getRiskLabel = (risk) => {
    if (risk > 0.7) return t('common.highRisk');
    if (risk > 0.4) return t('common.mediumRisk');
    return t('common.lowRisk');
  };

  return (
    <div className="pt-24 min-h-screen bg-gradient-to-br from-cyan-400 via-blue-500 to-purple-600 pb-12">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center text-white mb-12"
        >
          <h1 className="text-5xl font-bold mb-4">{t('kidney.title')}</h1>
          <p className="text-xl text-blue-100">{t('kidney.description')}</p>
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
                    {t('kidney.labels.age')}
                  </label>
                  <input
                    type="number"
                    name="age"
                    value={formData.age}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="e.g. 45"
                    min="0"
                    max="150"
                  />
                </div>
                <div>
                  <label className="block text-white font-semibold mb-2">
                    {t('kidney.labels.bloodPressure')}
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="number"
                      name="systolicBP"
                      value={formData.systolicBP}
                      onChange={handleInputChange}
                      className="w-1/2 px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                      placeholder="Systolic"
                      min="0"
                      max="300"
                    />
                    <input
                      type="number"
                      name="diastolicBP"
                      value={formData.diastolicBP}
                      onChange={handleInputChange}
                      className="w-1/2 px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                      placeholder="Diastolic"
                      min="0"
                      max="300"
                    />
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-white font-semibold mb-2">
                    {t('kidney.labels.glucose')}
                  </label>
                  <input
                    type="number"
                    name="glucose"
                    value={formData.glucose}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="e.g. 100"
                    min="0"
                    step="1"
                  />
                </div>
                <div>
                  <label className="block text-white font-semibold mb-2">
                    {t('kidney.labels.potassium')}
                  </label>
                  <input
                    type="number"
                    name="potassium"
                    value={formData.potassium}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="e.g. 4.5"
                    step="0.1"
                    min="0"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-white font-semibold mb-2">
                    {t('kidney.labels.creatinine')}
                  </label>
                  <input
                    type="number"
                    name="creatinine"
                    value={formData.creatinine}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="e.g. 0.9"
                    step="0.1"
                    min="0"
                  />
                </div>
                <div>
                  <label className="block text-white font-semibold mb-2">
                    {t('kidney.labels.bmi')}
                  </label>
                  <input
                    type="number"
                    name="bmi"
                    value={formData.bmi}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="e.g. 24.5"
                    step="0.1"
                    min="0"
                  />
                </div>
              </div>

              <div>
                <label className="block text-white font-semibold mb-2">
                  {t('kidney.labels.smokingStatus')}
                </label>
                <select
                  name="smokingStatus"
                  value={formData.smokingStatus}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all"
                >
                  <option value="no">No</option>
                  <option value="yes">Yes</option>
                  <option value="former">Former Smoker</option>
                </select>
              </div>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-bold rounded-lg hover:shadow-lg transition-all disabled:opacity-50"
              >
                {loading ? t('common.loading') : t('kidney.predict')}
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
            <div className="h-80 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 overflow-hidden">
              {typeof MoleculeAnimation === 'function' ? (
                <MoleculeAnimation color="#00d9ff" />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-white">
                  Loading animation...
                </div>
              )}
            </div>

            {/* Results */}
            {kidneyResult && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className={`bg-gradient-to-br ${getRiskColor(kidneyResult.risk_score)} rounded-2xl p-8 text-white border border-white/20`}
              >
                <h3 className="text-2xl font-bold mb-4">{t('kidney.results')}</h3>
                
                <div className="space-y-4">
                  <div>
                    <p className="text-white/80">Risk Level</p>
                    <p className="text-3xl font-bold">{getRiskLabel(kidneyResult.risk_score)}</p>
                  </div>

                  <div>
                    <p className="text-white/80">Confidence</p>
                    <div className="bg-white/20 rounded-full h-2 mt-2 overflow-hidden">
                      <div
                        className="bg-white h-full transition-all duration-500"
                        style={{ width: `${Math.min((kidneyResult.confidence ?? 0.82) * 100, 100)}%` }}
                      />
                    </div>
                    <p className="text-sm mt-2">{((kidneyResult.confidence ?? 0.82) * 100).toFixed(1)}%</p>
                  </div>

                  <div className="pt-4 border-t border-white/20">
                    <p className="font-semibold mb-2">{t('common.recommendation')}</p>
                    <p className="text-white/90">
                      {kidneyResult.risk_score > 0.7
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
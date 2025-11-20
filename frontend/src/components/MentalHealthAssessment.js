import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { useStore } from '../store/store';
import { mentalHealthAPI } from '../api/api';
import { toast } from 'react-toastify';
import { RotatingBox } from './3D/RotatingBox';

export const MentalHealthAssessment = () => {
  const { t } = useTranslation();
  const { setLoading, loading, setMentalHealthResult, mentalHealthResult } = useStore();

  const [formData, setFormData] = useState({
    stressLevel: 5,
    sleepHours: 7,
    exerciseFrequency: 3,
    socialInteraction: 6,
    workHoursPerWeek: 40,
    dietQuality: 6,
    mentalHealthHistory: 'no'
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSliderChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: parseInt(value)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    setLoading(true);
    try {
      const response = await mentalHealthAPI.predict(formData);
      setMentalHealthResult(response.data);
      toast.success(t('common.success'));
    } catch (error) {
      toast.error('Assessment failed. Please try again.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const getWellnessColor = (score) => {
    if (score > 0.7) return 'from-green-500 to-emerald-600';
    if (score > 0.4) return 'from-yellow-500 to-orange-600';
    return 'from-red-500 to-pink-600';
  };

  const getWellnessLabel = (score) => {
    if (score > 0.7) return 'Good';
    if (score > 0.4) return 'Fair';
    return 'Needs Attention';
  };

  return (
    <div className="pt-24 min-h-screen bg-gradient-to-br from-purple-500 via-indigo-500 to-blue-600 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center text-white mb-12"
        >
          <h1 className="text-5xl font-bold mb-4">{t('mental.title')}</h1>
          <p className="text-xl text-indigo-100">{t('mental.description')}</p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Form */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20"
            style={{ maxHeight: '600px', overflowY: 'auto' }}
          >
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Stress Level Slider */}
              <div>
                <label className="block text-white font-semibold mb-3">
                  {t('mental.labels.stressLevel')} - <span className="text-yellow-200">{formData.stressLevel}</span>
                </label>
                <input
                  type="range"
                  name="stressLevel"
                  min="0"
                  max="10"
                  value={formData.stressLevel}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-white"
                />
              </div>

              {/* Sleep Hours */}
              <div>
                <label className="block text-white font-semibold mb-3">
                  {t('mental.labels.sleepHours')} - <span className="text-blue-200">{formData.sleepHours}h</span>
                </label>
                <input
                  type="range"
                  name="sleepHours"
                  min="0"
                  max="12"
                  value={formData.sleepHours}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-white"
                />
              </div>

              {/* Exercise Frequency */}
              <div>
                <label className="block text-white font-semibold mb-3">
                  {t('mental.labels.exerciseFrequency')} - <span className="text-green-200">{formData.exerciseFrequency} days</span>
                </label>
                <input
                  type="range"
                  name="exerciseFrequency"
                  min="0"
                  max="7"
                  value={formData.exerciseFrequency}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-white"
                />
              </div>

              {/* Social Interaction */}
              <div>
                <label className="block text-white font-semibold mb-3">
                  {t('mental.labels.socialInteraction')} - <span className="text-pink-200">{formData.socialInteraction}</span>
                </label>
                <input
                  type="range"
                  name="socialInteraction"
                  min="0"
                  max="10"
                  value={formData.socialInteraction}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-white"
                />
              </div>

              {/* Work Hours */}
              <div>
                <label className="block text-white font-semibold mb-3">
                  {t('mental.labels.workHoursPerWeek')} - <span className="text-orange-200">{formData.workHoursPerWeek}h</span>
                </label>
                <input
                  type="range"
                  name="workHoursPerWeek"
                  min="0"
                  max="80"
                  value={formData.workHoursPerWeek}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-white"
                />
              </div>

              {/* Diet Quality */}
              <div>
                <label className="block text-white font-semibold mb-3">
                  {t('mental.labels.dietQuality')} - <span className="text-purple-200">{formData.dietQuality}</span>
                </label>
                <input
                  type="range"
                  name="dietQuality"
                  min="0"
                  max="10"
                  value={formData.dietQuality}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-white"
                />
              </div>

              {/* Mental Health History */}
              <div>
                <label className="block text-white font-semibold mb-3">
                  {t('mental.labels.mentalHealthHistory')}
                </label>
                <select
                  name="mentalHealthHistory"
                  value={formData.mentalHealthHistory}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all appearance-none cursor-pointer"
                >
                  <option value="no">No</option>
                  <option value="yes">Yes</option>
                  <option value="family">Family History</option>
                </select>
              </div>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-gradient-to-r from-purple-500 to-indigo-600 text-white font-bold rounded-lg hover:shadow-lg transition-all disabled:opacity-50 mt-6"
              >
                {loading ? t('common.loading') : t('mental.predict')}
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
              <RotatingBox color="#a78bfa" size={1.5} />
            </div>

            {/* Results */}
            {mentalHealthResult && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className={`bg-gradient-to-br ${getWellnessColor(mentalHealthResult.wellness_score)} rounded-2xl p-8 text-white border border-white/20 shadow-2xl`}
              >
                <h3 className="text-2xl font-bold mb-6">{t('mental.results')}</h3>
                
                <div className="space-y-6">
                  <div>
                    <p className="text-white/80 text-sm mb-2">Wellness Status</p>
                    <p className="text-4xl font-bold">{getWellnessLabel(mentalHealthResult.wellness_score)}</p>
                  </div>

                  <div>
                    <p className="text-white/80 text-sm mb-2">Overall Score</p>
                    <div className="bg-white/20 rounded-full h-4 mt-2 overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${(mentalHealthResult.wellness_score || 0.6) * 100}%` }}
                        transition={{ duration: 1, ease: 'easeInOut' }}
                        className="bg-white h-full transition-all"
                      />
                    </div>
                    <p className="text-sm mt-3 font-semibold">{((mentalHealthResult.wellness_score || 0.6) * 100).toFixed(1)}%</p>
                  </div>

                  <div className="pt-6 border-t border-white/30">
                    <p className="font-semibold mb-3">💡 {t('common.recommendation')}</p>
                    <p className="text-white/90 leading-relaxed">
                      {mentalHealthResult.wellness_score < 0.4
                        ? 'Consider speaking with a mental health professional. Your wellness needs attention.'
                        : mentalHealthResult.wellness_score < 0.7
                        ? 'Try to maintain healthy habits. Consider small lifestyle improvements.'
                        : 'Great! Keep maintaining your healthy lifestyle and mental wellness.'}
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
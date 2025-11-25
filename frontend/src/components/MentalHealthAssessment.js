import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { useStore } from '../store/store';
import { mentalHealthAPI } from '../api/api';
import { toast } from 'react-toastify';
import { RotatingBox } from './3D/RotatingBox';
import { SelectDropdown } from './SelectDropdown';

export const MentalHealthAssessment = () => {
  const { t } = useTranslation();
  const { setLoading, loading, user } = useStore();
  const [result, setResult] = useState(null);

  const [formData, setFormData] = useState({
    age: '',
    gender: '',
    employment: '',
    work_env: '',
    stress: 5,
    sleep: 7,
    activity: 3,
    depression: 5,
    anxiety: 5,
    support: 5,
    productivity: 5,
    mh_history: '',
    treatment: ''
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

  const savePredictionToHistory = (prediction) => {
    try {
      const userId = user?.id || 'anonymous';
      const key = `predictionHistory_${userId}`;
      const history = JSON.parse(localStorage.getItem(key) || '[]');
      
      const newPrediction = {
        id: Math.random().toString(36).substr(2, 9),
        disease: 'mental_health',
        timestamp: new Date().toISOString(),
        riskScore: prediction.assessment_score || 0,
        prediction: prediction.predicted_class,
        details: formData
      };
      
      history.push(newPrediction);
      localStorage.setItem(key, JSON.stringify(history));
    } catch (error) {
      console.error('Error saving prediction:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    setResult(null);
    setLoading(true);
    
    try {
      const response = await mentalHealthAPI.predict(formData);
      const newResult = response.data;
      setResult(newResult);
      savePredictionToHistory(newResult);
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
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center text-white mb-12"
        >
          <h1 className="text-5xl font-bold mb-4">{t('mental.title')}</h1>
          <p className="text-xl text-indigo-100">{t('mental.description')}</p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20"
            style={{ maxHeight: '700px', overflowY: 'auto' }}
          >
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-white font-semibold mb-2">Age</label>
                  <input
                    type="number"
                    name="age"
                    value={formData.age}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="30"
                  />
                </div>
                <div>
                  <label className="block text-white font-semibold mb-2">Gender</label>
                  <select
                    name="gender"
                    value={formData.gender}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all"
                  >
                    <option value="">Select Gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-white font-semibold mb-2">Employment</label>
                  <select
                    name="employment"
                    value={formData.employment}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all"
                  >
                    <option value="">Select</option>
                    <option value="employed">Employed</option>
                    <option value="unemployed">Unemployed</option>
                    <option value="student">Student</option>
                    <option value="retired">Retired</option>
                  </select>
                </div>
                <div>
                  <label className="block text-white font-semibold mb-2">Work Environment</label>
                  <select
                    name="work_env"
                    value={formData.work_env}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all"
                  >
                    <option value="">Select</option>
                    <option value="remote">Remote</option>
                    <option value="office">Office</option>
                    <option value="hybrid">Hybrid</option>
                    <option value="n/a">N/A</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-white font-semibold mb-3">
                  Stress Level - <span className="text-yellow-200">{formData.stress}</span>
                </label>
                <input
                  type="range"
                  name="stress"
                  min="0"
                  max="10"
                  value={formData.stress}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-white"
                />
              </div>

              <div>
                <label className="block text-white font-semibold mb-3">
                  Sleep Hours - <span className="text-blue-200">{formData.sleep}h</span>
                </label>
                <input
                  type="range"
                  name="sleep"
                  min="0"
                  max="12"
                  value={formData.sleep}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-white"
                />
              </div>

              <div>
                <label className="block text-white font-semibold mb-3">
                  Activity (days/week) - <span className="text-green-200">{formData.activity}</span>
                </label>
                <input
                  type="range"
                  name="activity"
                  min="0"
                  max="7"
                  value={formData.activity}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-white"
                />
              </div>

              <div>
                <label className="block text-white font-semibold mb-3">
                  Depression Score - <span className="text-pink-200">{formData.depression}</span>
                </label>
                <input
                  type="range"
                  name="depression"
                  min="0"
                  max="10"
                  value={formData.depression}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-white"
                />
              </div>

              <div>
                <label className="block text-white font-semibold mb-3">
                  Anxiety Score - <span className="text-orange-200">{formData.anxiety}</span>
                </label>
                <input
                  type="range"
                  name="anxiety"
                  min="0"
                  max="10"
                  value={formData.anxiety}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-white"
                />
              </div>

              <div>
                <label className="block text-white font-semibold mb-3">
                  Social Support - <span className="text-purple-200">{formData.support}</span>
                </label>
                <input
                  type="range"
                  name="support"
                  min="0"
                  max="10"
                  value={formData.support}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-white"
                />
              </div>

              <div>
                <label className="block text-white font-semibold mb-3">
                  Productivity - <span className="text-indigo-200">{formData.productivity}</span>
                </label>
                <input
                  type="range"
                  name="productivity"
                  min="0"
                  max="10"
                  value={formData.productivity}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-white"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-white font-semibold mb-2">Mental Health History</label>
                  <select
                    name="mh_history"
                    value={formData.mh_history}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all"
                  >
                    <option value="">Select</option>
                    <option value="yes">Yes</option>
                    <option value="no">No</option>
                    <option value="family">Family History</option>
                  </select>
                </div>
                <div>
                  <label className="block text-white font-semibold mb-2">Seeking Treatment</label>
                  <select
                    name="treatment"
                    value={formData.treatment}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all"
                  >
                    <option value="">Select</option>
                    <option value="yes">Yes</option>
                    <option value="no">No</option>
                    <option value="considering">Considering</option>
                  </select>
                </div>
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

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex flex-col gap-8"
          >
            <div className="w-full h-80 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 overflow-hidden shadow-2xl">
              <RotatingBox color="#a78bfa" size={1.5} />
            </div>

            {result && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className={`bg-gradient-to-br ${getWellnessColor(result.assessment_score)} rounded-2xl p-8 text-white border border-white/20 shadow-2xl`}
              >
                <h3 className="text-2xl font-bold mb-6">{t('mental.results')}</h3>
                
                <div className="space-y-6">
                  <div>
                    <p className="text-white/80 text-sm mb-2">Wellness Status</p>
                    <p className="text-4xl font-bold">{getWellnessLabel(result.assessment_score)}</p>
                  </div>

                  <div>
                    <p className="text-white/80 text-sm mb-2">Overall Score</p>
                    <div className="bg-white/20 rounded-full h-4 mt-2 overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${(result.assessment_score || 0.5) * 100}%` }}
                        transition={{ duration: 1, ease: 'easeInOut' }}
                        className="bg-white h-full"
                      />
                    </div>
                    <p className="text-sm mt-3 font-semibold">{((result.assessment_score || 0.5) * 100).toFixed(1)}%</p>
                  </div>

                  <div className="pt-6 border-t border-white/30">
                    <p className="font-semibold mb-3">💡 {t('common.recommendation')}</p>
                    <p className="text-white/90 leading-relaxed">
                      {result.assessment_score < 0.4
                        ? 'Consider speaking with a mental health professional. Your wellness needs attention.'
                        : result.assessment_score < 0.7
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

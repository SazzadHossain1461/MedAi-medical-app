import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { useStore } from '../store/store';
import { mentalHealthAPI } from '../api/api';
import { toast } from 'react-toastify';
import { RotatingBox } from './3D/RotatingBox';

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
      toast.success(t('mental.success'));
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
        
        {/* ===== HEADER SECTION ===== */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center text-white mb-12"
        >
          <h1 className="text-5xl font-bold mb-4">{t('mental.title')}</h1>
          <p className="text-xl text-indigo-100">{t('mental.description')}</p>
        </motion.div>

        {/* ===== MAIN CONTENT GRID ===== */}
        <div className="grid md:grid-cols-2 gap-8">
          
          {/* ===== LEFT COLUMN - FORM ===== */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20"
            style={{ maxHeight: '800px', overflowY: 'auto' }}
          >
            <form onSubmit={handleSubmit} className="space-y-6">
              
              {/* ===== DEMOGRAPHICS SECTION ===== */}
              <div className="border-b border-white/20 pb-4">
                <h3 className="text-white font-bold mb-4">👤 {t('mental.demographics')}</h3>
                <div className="grid grid-cols-2 gap-4">
                  {/* Age Input */}
                  <div>
                    <label className="block text-white font-semibold mb-2">
                      {t('mental.age')}
                    </label>
                    <input
                      type="number"
                      name="age"
                      value={formData.age}
                      onChange={handleInputChange}
                      min="0"
                      max="120"
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                      placeholder="30"
                    />
                  </div>

                  {/* Gender Select */}
                  <div>
                    <label className="block text-white font-semibold mb-2">
                      {t('mental.gender')}
                    </label>
                    <select
                      name="gender"
                      value={formData.gender}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all appearance-none"
                      style={{
                        backgroundImage: `url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e")`,
                        backgroundRepeat: 'no-repeat',
                        backgroundPosition: 'right 0.5rem center',
                        backgroundSize: '1.5em 1.5em',
                        paddingRight: '2.5rem'
                      }}
                    >
                      <option value="">Select Gender</option>
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* ===== EMPLOYMENT SECTION ===== */}
              <div className="border-b border-white/20 pb-4">
                <h3 className="text-white font-bold mb-4">💼 {t('mental.employment')}</h3>
                <div className="grid grid-cols-2 gap-4">
                  {/* Employment Status */}
                  <div>
                    <label className="block text-white font-semibold mb-2">
                      {t('mental.employment')}
                    </label>
                    <select
                      name="employment"
                      value={formData.employment}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all appearance-none"
                      style={{
                        backgroundImage: `url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e")`,
                        backgroundRepeat: 'no-repeat',
                        backgroundPosition: 'right 0.5rem center',
                        backgroundSize: '1.5em 1.5em',
                        paddingRight: '2.5rem'
                      }}
                    >
                      <option value="">Select</option>
                      <option value="employed">Employed</option>
                      <option value="unemployed">Unemployed</option>
                      <option value="student">Student</option>
                      <option value="retired">Retired</option>
                    </select>
                  </div>

                  {/* Work Environment */}
                  <div>
                    <label className="block text-white font-semibold mb-2">
                      {t('mental.workEnvironment')}
                    </label>
                    <select
                      name="work_env"
                      value={formData.work_env}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all appearance-none"
                      style={{
                        backgroundImage: `url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e")`,
                        backgroundRepeat: 'no-repeat',
                        backgroundPosition: 'right 0.5rem center',
                        backgroundSize: '1.5em 1.5em',
                        paddingRight: '2.5rem'
                      }}
                    >
                      <option value="">Select</option>
                      <option value="remote">Remote</option>
                      <option value="office">Office</option>
                      <option value="hybrid">Hybrid</option>
                      <option value="n/a">N/A</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* ===== STRESS LEVEL SLIDER ===== */}
              <div className="border-b border-white/20 pb-4">
                <div className="flex justify-between items-center mb-3">
                  <label className="text-white font-semibold">
                    😰 {t('mental.stressLevel')}
                  </label>
                  <span className="text-yellow-200 font-bold text-lg">{formData.stress}/10</span>
                </div>
                <input
                  type="range"
                  name="stress"
                  min="0"
                  max="10"
                  value={formData.stress}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-yellow-300"
                />
                <p className="text-white/60 text-xs mt-2">0 = No Stress | 10 = Extreme Stress</p>
              </div>

              {/* ===== SLEEP HOURS SLIDER ===== */}
              <div className="border-b border-white/20 pb-4">
                <div className="flex justify-between items-center mb-3">
                  <label className="text-white font-semibold">
                    😴 {t('mental.sleepHours')}
                  </label>
                  <span className="text-blue-200 font-bold text-lg">{formData.sleep}h</span>
                </div>
                <input
                  type="range"
                  name="sleep"
                  min="0"
                  max="12"
                  value={formData.sleep}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-blue-300"
                />
                <p className="text-white/60 text-xs mt-2">Recommended: 7-9 hours</p>
              </div>

              {/* ===== ACTIVITY SLIDER ===== */}
              <div className="border-b border-white/20 pb-4">
                <div className="flex justify-between items-center mb-3">
                  <label className="text-white font-semibold">
                    🏃 {t('mental.activity')}
                  </label>
                  <span className="text-green-200 font-bold text-lg">{formData.activity}/7</span>
                </div>
                <input
                  type="range"
                  name="activity"
                  min="0"
                  max="7"
                  value={formData.activity}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-green-300"
                />
                <p className="text-white/60 text-xs mt-2">Days per week of physical activity</p>
              </div>

              {/* ===== DEPRESSION SLIDER ===== */}
              <div className="border-b border-white/20 pb-4">
                <div className="flex justify-between items-center mb-3">
                  <label className="text-white font-semibold">
                    😞 {t('mental.depressionScore')}
                  </label>
                  <span className="text-pink-200 font-bold text-lg">{formData.depression}/10</span>
                </div>
                <input
                  type="range"
                  name="depression"
                  min="0"
                  max="10"
                  value={formData.depression}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-pink-300"
                />
                <p className="text-white/60 text-xs mt-2">0 = Not at all | 10 = Severe</p>
              </div>

              {/* ===== ANXIETY SLIDER ===== */}
              <div className="border-b border-white/20 pb-4">
                <div className="flex justify-between items-center mb-3">
                  <label className="text-white font-semibold">
                    😟 {t('mental.anxietyScore')}
                  </label>
                  <span className="text-orange-200 font-bold text-lg">{formData.anxiety}/10</span>
                </div>
                <input
                  type="range"
                  name="anxiety"
                  min="0"
                  max="10"
                  value={formData.anxiety}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-orange-300"
                />
                <p className="text-white/60 text-xs mt-2">0 = Not at all | 10 = Severe</p>
              </div>

              {/* ===== SOCIAL SUPPORT SLIDER ===== */}
              <div className="border-b border-white/20 pb-4">
                <div className="flex justify-between items-center mb-3">
                  <label className="text-white font-semibold">
                    👥 {t('mental.socialSupport')}
                  </label>
                  <span className="text-purple-200 font-bold text-lg">{formData.support}/10</span>
                </div>
                <input
                  type="range"
                  name="support"
                  min="0"
                  max="10"
                  value={formData.support}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-purple-300"
                />
                <p className="text-white/60 text-xs mt-2">Support from family, friends, and community</p>
              </div>

              {/* ===== PRODUCTIVITY SLIDER ===== */}
              <div className="border-b border-white/20 pb-4">
                <div className="flex justify-between items-center mb-3">
                  <label className="text-white font-semibold">
                    ⚡ {t('mental.productivity')}
                  </label>
                  <span className="text-indigo-200 font-bold text-lg">{formData.productivity}/10</span>
                </div>
                <input
                  type="range"
                  name="productivity"
                  min="0"
                  max="10"
                  value={formData.productivity}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-indigo-300"
                />
                <p className="text-white/60 text-xs mt-2">Your overall productivity level</p>
              </div>

              {/* ===== MENTAL HEALTH HISTORY SECTION ===== */}
              <div className="border-b border-white/20 pb-4">
                <h3 className="text-white font-bold mb-4">🏥 {t('mental.mentalHealthHistory')}</h3>
                <div className="grid grid-cols-2 gap-4">
                  {/* Mental Health History */}
                  <div>
                    <label className="block text-white font-semibold mb-2 text-sm">
                      {t('mental.mentalHealthHistory')}
                    </label>
                    <select
                      name="mh_history"
                      value={formData.mh_history}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all appearance-none text-sm"
                      style={{
                        backgroundImage: `url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e")`,
                        backgroundRepeat: 'no-repeat',
                        backgroundPosition: 'right 0.5rem center',
                        backgroundSize: '1.5em 1.5em',
                        paddingRight: '2.5rem'
                      }}
                    >
                      <option value="">Select</option>
                      <option value="yes">Yes</option>
                      <option value="no">No</option>
                      <option value="family">Family History</option>
                    </select>
                  </div>

                  {/* Seeking Treatment */}
                  <div>
                    <label className="block text-white font-semibold mb-2 text-sm">
                      {t('mental.seekingTreatment')}
                    </label>
                    <select
                      name="treatment"
                      value={formData.treatment}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all appearance-none text-sm"
                      style={{
                        backgroundImage: `url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e")`,
                        backgroundRepeat: 'no-repeat',
                        backgroundPosition: 'right 0.5rem center',
                        backgroundSize: '1.5em 1.5em',
                        paddingRight: '2.5rem'
                      }}
                    >
                      <option value="">Select</option>
                      <option value="yes">Yes</option>
                      <option value="no">No</option>
                      <option value="considering">Considering</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* ===== SUBMIT BUTTON ===== */}
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-gradient-to-r from-purple-500 to-indigo-600 text-white font-bold rounded-lg hover:shadow-lg transition-all disabled:opacity-50 mt-6"
              >
                {loading ? t('mental.loading') : `📋 ${t('mental.predict')}`}
              </motion.button>
            </form>
          </motion.div>

          {/* ===== RIGHT COLUMN - VISUALIZATION & RESULTS ===== */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex flex-col gap-8"
          >
            {/* 3D Animation Container */}
            <div className="w-full h-80 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 overflow-hidden shadow-2xl">
              <RotatingBox color="#a78bfa" size={1.5} />
            </div>

            {/* Results Card - Shows only when result exists */}
            {result && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className={`bg-gradient-to-br ${getWellnessColor(result.assessment_score)} rounded-2xl p-8 text-white border border-white/20 shadow-2xl`}
              >
                <h3 className="text-2xl font-bold mb-6">🎯 {t('mental.results')}</h3>
                
                <div className="space-y-6">
                  {/* Wellness Status Display */}
                  <div>
                    <p className="text-white/80 text-sm mb-2">{t('mental.wellnessStatus')}</p>
                    <p className="text-4xl font-bold">{getWellnessLabel(result.assessment_score)}</p>
                  </div>

                  {/* Overall Score with Progress Bar */}
                  <div>
                    <p className="text-white/80 text-sm mb-2">{t('mental.overallScore')}</p>
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

                  {/* Recommendations Section */}
                  <div className="pt-6 border-t border-white/30">
                    <p className="font-semibold mb-3">💡 {t('common.recommendation')}</p>
                    <p className="text-white/90 leading-relaxed text-sm">
                      {result.assessment_score < 0.4
                        ? t('mental.considerProfessional')
                        : result.assessment_score < 0.7
                        ? t('mental.maintainHabits')
                        : t('mental.keepMaintaining')}
                    </p>
                  </div>

                  {/* Additional Tips */}
                  <div className="pt-4 border-t border-white/30">
                    <p className="font-semibold mb-2">✨ Wellness Tips</p>
                    <div className="text-white/90 text-xs space-y-1">
                      <p>• Take regular breaks during work</p>
                      <p>• Engage in physical activities you enjoy</p>
                      <p>• Maintain healthy relationships</p>
                      <p>• Practice mindfulness or meditation</p>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </motion.div>
        </div>
      </div>

      <style jsx>{`
        select {
          appearance: none;
        }

        select option {
          background: #1a1a2e;
          color: white;
          padding: 10px;
          margin: 5px 0;
        }

        select option:hover {
          background: #667eea;
          color: white;
        }

        select:focus {
          outline: none;
          border-color: white;
        }

        input[type="range"]::-webkit-slider-thumb {
          appearance: none;
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: white;
          cursor: pointer;
          box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        }

        input[type="range"]::-moz-range-thumb {
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: white;
          cursor: pointer;
          border: none;
          box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        }
      `}</style>
    </div>
  );
};
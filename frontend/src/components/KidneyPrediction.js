import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { useStore } from '../store/store';
import { kidneyAPI } from '../api/api';
import { toast } from 'react-toastify';
import { MoleculeAnimation } from './3D/MoleculeAnimation';

export const KidneyPrediction = () => {
  const { t } = useTranslation();
  const { setLoading, loading, user } = useStore();
  const [result, setResult] = useState(null);

  const [formData, setFormData] = useState({
    age: '45',
    bp: '140',
    sg: '1.020',
    al: '0',
    su: '0',
    bgr: '120',
    bu: '25',
    sc: '1.2',
    sod: '138',
    pot: '5.2',
    hemo: '10.5',
    pcv: '35',
    wc: '8000'
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const savePredictionToHistory = (prediction) => {
    try {
      const userId = user?.id || 'anonymous';
      const key = `predictionHistory_${userId}`;
      const history = JSON.parse(localStorage.getItem(key) || '[]');
      
      const newPrediction = {
        id: Math.random().toString(36).substr(2, 9),
        disease: 'kidney',
        timestamp: new Date().toISOString(),
        riskScore: prediction.probability || 0,
        prediction: prediction.prediction,
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
    
    if (!formData.age || !formData.sc || !formData.bp) {
      toast.error(t('common.error'));
      return;
    }

    setResult(null);
    setLoading(true);
    
    try {
      const numericFormData = {
        age: parseFloat(formData.age),
        bp: parseFloat(formData.bp),
        sg: parseFloat(formData.sg),
        al: parseFloat(formData.al),
        su: parseFloat(formData.su),
        bgr: parseFloat(formData.bgr),
        bu: parseFloat(formData.bu),
        sc: parseFloat(formData.sc),
        sod: parseFloat(formData.sod),
        pot: parseFloat(formData.pot),
        hemo: parseFloat(formData.hemo),
        pcv: parseFloat(formData.pcv),
        wc: parseFloat(formData.wc)
      };

      console.log('Sending kidney data:', numericFormData);
      
      const response = await kidneyAPI.predict(numericFormData);
      console.log('Kidney Response:', response.data);
      
      const newResult = {
        prediction: response.data.prediction || 0,
        probability: response.data.probability || response.data.confidence || 0.5,
        disease_status: response.data.disease_status || 'Unknown'
      };
      
      setResult(newResult);
      savePredictionToHistory(newResult);
      toast.success(t('kidney.success'));
    } catch (error) {
      console.error('Prediction error:', error);
      toast.error(error.response?.data?.error || 'Prediction failed. Please check your inputs.');
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

  const getCKDStage = (risk) => {
    if (risk > 0.9) return 'Stage 5 (ESRD)';
    if (risk > 0.7) return 'Stage 4 (Severe CKD)';
    if (risk > 0.5) return 'Stage 3b (Moderate CKD)';
    if (risk > 0.3) return 'Stage 3a (Mild-Moderate CKD)';
    return 'Stage 1-2 (Normal/Mild)';
  };

  return (
    <div className="pt-24 min-h-screen bg-gradient-to-br from-cyan-400 via-blue-500 to-purple-600 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center text-white mb-12"
        >
          <h1 className="text-5xl font-bold mb-4">{t('kidney.title')}</h1>
          <p className="text-xl text-blue-100">{t('kidney.subtitle')}</p>
        </motion.div>

        {/* Main Content Grid */}
        <div className="grid md:grid-cols-2 gap-8">
          
          {/* LEFT COLUMN - FORM */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20"
            style={{ maxHeight: '800px', overflowY: 'auto' }}
          >
            <form onSubmit={handleSubmit} className="space-y-5">
              
              {/* ===== DEMOGRAPHICS SECTION ===== */}
              <div className="border-b border-white/20 pb-4">
                <h3 className="text-white font-bold mb-4">👤 {t('kidney.demographics')}</h3>
                <div>
                  <label className="block text-white font-semibold mb-2">
                    {t('kidney.age')} *
                  </label>
                  <input
                    type="number"
                    name="age"
                    value={formData.age}
                    onChange={handleInputChange}
                    min="0"
                    max="120"
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="45"
                  />
                </div>
              </div>

              {/* ===== VITAL SIGNS SECTION ===== */}
              <div className="border-b border-white/20 pb-4">
                <h3 className="text-white font-bold mb-4">💊 {t('kidney.vitalSigns')}</h3>
                <div>
                  <label className="block text-white font-semibold mb-1 text-sm">
                    {t('kidney.bloodPressure')} *
                  </label>
                  <input
                    type="number"
                    name="bp"
                    value={formData.bp}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="120-140"
                  />
                  <p className="text-white/60 text-xs mt-1">Normal: Less than 120 mmHg</p>
                </div>
              </div>

              {/* ===== URINE ANALYSIS SECTION ===== */}
              <div className="border-b border-white/20 pb-4">
                <h3 className="text-white font-bold mb-4">🧬 {t('kidney.urineAnalysis')}</h3>
                <div className="grid grid-cols-2 gap-4">
                  {/* Specific Gravity */}
                  <div>
                    <label className="block text-white font-semibold mb-1 text-sm">
                      {t('kidney.specificGravity')}
                    </label>
                    <input
                      type="number"
                      name="sg"
                      value={formData.sg}
                      onChange={handleInputChange}
                      step="0.001"
                      min="1"
                      max="1.05"
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                      placeholder="1.020"
                    />
                    <p className="text-white/60 text-xs mt-1">Normal: 1.005-1.030</p>
                  </div>
                  {/* Protein in Urine */}
                  <div>
                    <label className="block text-white font-semibold mb-1 text-sm">
                      {t('kidney.proteinInUrine')}
                    </label>
                    <select
                      name="al"
                      value={formData.al}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all text-sm appearance-none"
                      style={{
                        backgroundImage: `url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e")`,
                        backgroundRepeat: 'no-repeat',
                        backgroundPosition: 'right 0.5rem center',
                        backgroundSize: '1.5em 1.5em',
                        paddingRight: '2.5rem'
                      }}
                    >
                      <option value="0">Absent</option>
                      <option value="1">Trace</option>
                      <option value="2">++</option>
                      <option value="3">+++</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* ===== URINE COMPONENTS SECTION ===== */}
              <div className="border-b border-white/20 pb-4">
                <h3 className="text-white font-bold mb-4">🔬 {t('kidney.urineComponents')}</h3>
                <div>
                  <label className="block text-white font-semibold mb-1 text-sm">
                    {t('kidney.sugarInUrine')}
                  </label>
                  <select
                    name="su"
                    value={formData.su}
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
                    <option value="0">Absent</option>
                    <option value="1">Present</option>
                  </select>
                </div>
              </div>

              {/* ===== BLOOD CHEMISTRY SECTION ===== */}
              <div className="border-b border-white/20 pb-4">
                <h3 className="text-white font-bold mb-4">🧪 {t('kidney.bloodChemistry')}</h3>
                <div className="grid grid-cols-2 gap-4">
                  {/* Fasting Glucose */}
                  <div>
                    <label className="block text-white font-semibold mb-1 text-sm">
                      {t('kidney.fastingGlucose')} *
                    </label>
                    <input
                      type="number"
                      name="bgr"
                      value={formData.bgr}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                      placeholder="120"
                    />
                    <p className="text-white/60 text-xs mt-1">Normal: 70-100 mg/dL</p>
                  </div>
                  {/* Blood Urea Nitrogen */}
                  <div>
                    <label className="block text-white font-semibold mb-1 text-sm">
                      {t('kidney.bloodUreaNitrogen')}
                    </label>
                    <input
                      type="number"
                      name="bu"
                      value={formData.bu}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                      placeholder="25"
                    />
                    <p className="text-white/60 text-xs mt-1">Normal: 7-20 mg/dL</p>
                  </div>
                </div>
              </div>

              {/* ===== KIDNEY FUNCTION SECTION ===== */}
              <div className="border-b border-white/20 pb-4">
                <h3 className="text-white font-bold mb-4">🫀 {t('kidney.kidneyFunction')}</h3>
                <div>
                  <label className="block text-white font-semibold mb-1 text-sm">
                    {t('kidney.serumCreatinine')} *
                  </label>
                  <input
                    type="number"
                    name="sc"
                    value={formData.sc}
                    onChange={handleInputChange}
                    step="0.1"
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="0.9"
                  />
                  <p className="text-white/60 text-xs mt-1">Normal: 0.7-1.3 mg/dL (Higher = Reduced kidney function)</p>
                </div>
              </div>

              {/* ===== ELECTROLYTES SECTION ===== */}
              <div className="border-b border-white/20 pb-4">
                <h3 className="text-white font-bold mb-4">⚡ {t('kidney.electrolytes')}</h3>
                <div className="grid grid-cols-2 gap-4">
                  {/* Sodium */}
                  <div>
                    <label className="block text-white font-semibold mb-1 text-sm">
                      {t('kidney.sodium')}
                    </label>
                    <input
                      type="number"
                      name="sod"
                      value={formData.sod}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                      placeholder="138"
                    />
                    <p className="text-white/60 text-xs mt-1">Normal: 136-145 mEq/L</p>
                  </div>
                  {/* Potassium */}
                  <div>
                    <label className="block text-white font-semibold mb-1 text-sm">
                      {t('kidney.potassium')}
                    </label>
                    <input
                      type="number"
                      name="pot"
                      value={formData.pot}
                      onChange={handleInputChange}
                      step="0.1"
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                      placeholder="5.2"
                    />
                    <p className="text-white/60 text-xs mt-1">Normal: 3.5-5.0 mEq/L</p>
                  </div>
                </div>
              </div>

              {/* ===== COMPLETE BLOOD COUNT SECTION ===== */}
              <div>
                <h3 className="text-white font-bold mb-4">🔴 {t('kidney.completeBloodCount')}</h3>
                <div className="grid grid-cols-3 gap-3">
                  {/* Hemoglobin */}
                  <div>
                    <label className="block text-white font-semibold mb-1 text-sm">
                      {t('kidney.hemoglobin')}
                    </label>
                    <input
                      type="number"
                      name="hemo"
                      value={formData.hemo}
                      onChange={handleInputChange}
                      step="0.1"
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                      placeholder="10.5"
                    />
                    <p className="text-white/60 text-xs mt-1">M: 13.5-17.5</p>
                  </div>
                  {/* Hematocrit */}
                  <div>
                    <label className="block text-white font-semibold mb-1 text-sm">
                      {t('kidney.hematocrit')}
                    </label>
                    <input
                      type="number"
                      name="pcv"
                      value={formData.pcv}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                      placeholder="35"
                    />
                    <p className="text-white/60 text-xs mt-1">M: 41-50%</p>
                  </div>
                  {/* WBC Count */}
                  <div>
                    <label className="block text-white font-semibold mb-1 text-sm">
                      {t('kidney.wbcCount')}
                    </label>
                    <input
                      type="number"
                      name="wc"
                      value={formData.wc}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                      placeholder="8000"
                    />
                    <p className="text-white/60 text-xs mt-1">Normal: 4500-11000</p>
                  </div>
                </div>
              </div>

              {/* ===== SUBMIT BUTTON ===== */}
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-bold rounded-lg hover:shadow-lg transition-all disabled:opacity-50"
              >
                {loading ? t('kidney.analyzing') : `🔍 ${t('kidney.getPrediction')}`}
              </motion.button>

              <p className="text-white/60 text-xs">{t('kidney.requiredFields')}</p>
            </form>
          </motion.div>

          {/* RIGHT COLUMN - VISUALIZATION & RESULTS */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex flex-col gap-8"
          >
            {/* 3D Animation Container */}
            <div className="h-80 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 overflow-hidden">
              <MoleculeAnimation color="#00d9ff" />
            </div>

            {/* Results Card - Shows only when result exists */}
            {result && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className={`bg-gradient-to-br ${getRiskColor(result.probability || 0)} rounded-2xl p-8 text-white border border-white/20 shadow-2xl`}
              >
                <h3 className="text-2xl font-bold mb-4">🎯 {t('kidney.predictResults')}</h3>
                
                <div className="space-y-4">
                  {/* Risk Level Display */}
                  <div>
                    <p className="text-white/80 text-sm">{t('kidney.riskLevel')}</p>
                    <p className="text-3xl font-bold">{getRiskLabel(result.probability || 0)}</p>
                  </div>

                  {/* CKD Stage */}
                  <div>
                    <p className="text-white/80 text-sm">{t('kidney.ckdStage')}</p>
                    <p className="text-xl font-bold">{getCKDStage(result.probability || 0)}</p>
                  </div>

                  {/* Confidence Score with Progress Bar */}
                  <div>
                    <p className="text-white/80 text-sm">{t('kidney.confidenceScore')}</p>
                    <div className="bg-white/20 rounded-full h-2 mt-2 overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${Math.min((result.probability || 0) * 100, 100)}%` }}
                        transition={{ duration: 1, ease: 'easeInOut' }}
                        className="bg-white h-full"
                      />
                    </div>
                    <p className="text-sm mt-2">{((result.probability || 0) * 100).toFixed(1)}%</p>
                  </div>

                  {/* Recommendations Section */}
                  <div className="pt-4 border-t border-white/20">
                    <p className="font-semibold mb-2">💡 {t('common.recommendation')}</p>
                    <div className="text-white/90 text-sm space-y-1">
                      {result.probability > 0.7 ? (
                        <>
                          <p>✓ {t('kidney.scheduleUrgent')}</p>
                          <p>✓ {t('kidney.getComprehensive')}</p>
                          <p>✓ {t('kidney.monitorBloodPressure')}</p>
                          <p>✓ {t('kidney.reduceSodium')}</p>
                        </>
                      ) : result.probability > 0.4 ? (
                        <>
                          <p>✓ {t('kidney.scheduleWithin2Weeks')}</p>
                          <p>✓ {t('kidney.monitorVitalSigns')}</p>
                          <p>✓ {t('kidney.maintainHealthy')}</p>
                        </>
                      ) : (
                        <>
                          <p>✓ {t('kidney.annualScreening')}</p>
                          <p>✓ {t('kidney.healthyDiet')}</p>
                          <p>✓ {t('kidney.regularCheckups')}</p>
                        </>
                      )}
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
          background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
          background-repeat: no-repeat;
          background-position: right 0.5rem center;
          background-size: 1.5em 1.5em;
          padding-right: 2.5rem;
        }

        select option {
          background: #1a1a2e;
          color: white;
          padding: 10px;
          margin: 5px 0;
        }

        select option:hover {
          background: #367dd3;
          color: white;
        }

        select:focus {
          outline: none;
          border-color: white;
        }
      `}</style>
    </div>
  );
};
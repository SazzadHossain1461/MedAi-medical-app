import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { useStore } from '../store/store';
import { dengueAPI } from '../api/api';
import { toast } from 'react-toastify';
import { HeartBeat } from './3D/HeartBeat';
import { SelectDropdown } from './SelectDropdown';

export const DenguePrediction = () => {
  const { t } = useTranslation();
  const { setLoading, loading, user } = useStore();
  const [result, setResult] = useState(null);

  const [formData, setFormData] = useState({
    Age: '30',
    Gender: '1',
    NS1: '0',
    IgG: '0',
    IgM: '0',
    Area: '1',
    AreaType: '1',
    HouseType: '1',
    District_encoded: '1',
    Temperature: '37.5',
    Symptoms: '0',
    Platelet_Count: '150000',
    WBC_Count: '7500'
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
        disease: 'dengue',
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
    
    if (!formData.Age || !formData.Temperature) {
      toast.error('Please fill all required fields');
      return;
    }

    setResult(null);
    setLoading(true);
    
    try {
      // Convert all values to numbers for API
      const numericFormData = {
        Age: parseFloat(formData.Age),
        Gender: parseFloat(formData.Gender),
        NS1: parseFloat(formData.NS1),
        IgG: parseFloat(formData.IgG),
        IgM: parseFloat(formData.IgM),
        Area: parseFloat(formData.Area),
        AreaType: parseFloat(formData.AreaType),
        HouseType: parseFloat(formData.HouseType),
        District_encoded: parseFloat(formData.District_encoded),
        Temperature: parseFloat(formData.Temperature),
        Symptoms: parseFloat(formData.Symptoms),
        Platelet_Count: parseFloat(formData.Platelet_Count),
        WBC_Count: parseFloat(formData.WBC_Count)
      };

      console.log('Sending data:', numericFormData);
      
      const response = await dengueAPI.predict(numericFormData);
      console.log('Response:', response.data);
      
      const newResult = {
        prediction: response.data.prediction || 0,
        probability: response.data.probability || response.data.confidence || 0.5,
        risk_level: response.data.risk_level || 'Unknown',
        recommendations: response.data.recommendations || []
      };
      
      setResult(newResult);
      savePredictionToHistory(newResult);
      toast.success('Prediction successful!');
    } catch (error) {
      console.error('Prediction error:', error);
      toast.error(error.response?.data?.error || 'Prediction failed. Please check your inputs.');
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
    if (risk > 0.7) return 'High Risk';
    if (risk > 0.4) return 'Medium Risk';
    return 'Low Risk';
  };

  return (
    <div className="pt-24 min-h-screen bg-gradient-to-br from-red-400 via-pink-500 to-purple-600 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center text-white mb-12"
        >
          <h1 className="text-5xl font-bold mb-4">Dengue Risk Prediction</h1>
          <p className="text-xl text-red-100">Assess your dengue risk based on medical parameters</p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20"
            style={{ maxHeight: '800px', overflowY: 'auto' }}
          >
            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Demographics */}
              <div className="border-b border-white/20 pb-4">
                <h3 className="text-white font-bold mb-4">📋 Demographics</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-white font-semibold mb-2">Age (years) *</label>
                    <input
                      type="number"
                      name="Age"
                      value={formData.Age}
                      onChange={handleInputChange}
                      min="0"
                      max="120"
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                      placeholder="30"
                    />
                  </div>
                  <div>
                    <label className="block text-white font-semibold mb-2">Gender *</label>
                    <select
                      name="Gender"
                      value={formData.Gender}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all"
                    >
                      <option value="0">Female</option>
                      <option value="1">Male</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Medical Parameters */}
              <div className="border-b border-white/20 pb-4">
                <h3 className="text-white font-bold mb-4">🩺 Medical Parameters</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-white font-semibold mb-1 text-sm">Temperature (°C) *</label>
                    <input
                      type="number"
                      name="Temperature"
                      value={formData.Temperature}
                      onChange={handleInputChange}
                      min="35"
                      max="42"
                      step="0.1"
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                      placeholder="37.5"
                    />
                    <p className="text-white/60 text-xs mt-1">Normal: 36.5-37.5°C</p>
                  </div>
                  <div>
                    <label className="block text-white font-semibold mb-1 text-sm">Platelet Count *</label>
                    <input
                      type="number"
                      name="Platelet_Count"
                      value={formData.Platelet_Count}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                      placeholder="150000"
                    />
                    <p className="text-white/60 text-xs mt-1">Normal: 150,000-400,000</p>
                  </div>
                </div>
              </div>

              {/* Blood Tests */}
              <div className="border-b border-white/20 pb-4">
                <h3 className="text-white font-bold mb-4">🧪 Blood Tests</h3>
                <div className="grid grid-cols-3 gap-3">
                  <div>
                    <label className="block text-white font-semibold mb-1 text-sm">NS1 Antigen</label>
                    <select
                      name="NS1"
                      value={formData.NS1}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all text-sm"
                    >
                      <option value="0">Negative</option>
                      <option value="1">Positive</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-white font-semibold mb-1 text-sm">IgG Antibody</label>
                    <select
                      name="IgG"
                      value={formData.IgG}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all text-sm"
                    >
                      <option value="0">Negative</option>
                      <option value="1">Positive</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-white font-semibold mb-1 text-sm">IgM Antibody</label>
                    <select
                      name="IgM"
                      value={formData.IgM}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all text-sm"
                    >
                      <option value="0">Negative</option>
                      <option value="1">Positive</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* WBC Count */}
              <div className="border-b border-white/20 pb-4">
                <h3 className="text-white font-bold mb-4">📊 Blood Count</h3>
                <div>
                  <label className="block text-white font-semibold mb-1 text-sm">WBC Count (cells/mm³) *</label>
                  <input
                    type="number"
                    name="WBC_Count"
                    value={formData.WBC_Count}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="7500"
                  />
                  <p className="text-white/60 text-xs mt-1">Normal: 4,500-11,000 cells/mm³</p>
                </div>
              </div>

              {/* Location & Environment */}
              <div className="border-b border-white/20 pb-4">
                <h3 className="text-white font-bold mb-4">📍 Location & Environment</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-white font-semibold mb-1 text-sm">Area Type</label>
                    <select
                      name="AreaType"
                      value={formData.AreaType}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all"
                    >
                      <option value="0">Rural</option>
                      <option value="1">Urban</option>
                      <option value="2">Suburban</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-white font-semibold mb-1 text-sm">House Type</label>
                    <select
                      name="HouseType"
                      value={formData.HouseType}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all"
                    >
                      <option value="0">Apartment</option>
                      <option value="1">House</option>
                      <option value="2">Hut</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Symptoms */}
              <div>
                <h3 className="text-white font-bold mb-4">🤒 Symptoms</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-white font-semibold mb-1 text-sm">Has Symptoms</label>
                    <select
                      name="Symptoms"
                      value={formData.Symptoms}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all"
                    >
                      <option value="0">No</option>
                      <option value="1">Yes (Fever, Headache, Pain)</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-white font-semibold mb-1 text-sm">District Code</label>
                    <select
                      name="District_encoded"
                      value={formData.District_encoded}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:border-white/60 transition-all"
                    >
                      <option value="0">Dhaka</option>
                      <option value="1">Chittagong</option>
                      <option value="2">Sylhet</option>
                      <option value="3">Khulna</option>
                      <option value="4">Rajshahi</option>
                      <option value="5">Barisal</option>
                    </select>
                  </div>
                </div>
              </div>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-gradient-to-r from-red-500 to-pink-600 text-white font-bold rounded-lg hover:shadow-lg transition-all disabled:opacity-50"
              >
                {loading ? 'Analyzing...' : '🔍 Get Prediction'}
              </motion.button>

              <p className="text-white/60 text-xs">* Required fields</p>
            </form>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex flex-col gap-8"
          >
            <div className="w-full h-80 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 overflow-hidden shadow-2xl">
              <HeartBeat color="#ff4444" />
            </div>

            {result && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className={`bg-gradient-to-br ${getRiskColor(result.probability || 0)} rounded-2xl p-8 text-white border border-white/20 shadow-2xl`}
              >
                <h3 className="text-2xl font-bold mb-6">🎯 Prediction Result</h3>
                
                <div className="space-y-6">
                  <div>
                    <p className="text-white/80 text-sm mb-2">Risk Level</p>
                    <p className="text-4xl font-bold">{getRiskLabel(result.probability || 0)}</p>
                  </div>

                  <div>
                    <p className="text-white/80 text-sm mb-2">Confidence Score</p>
                    <div className="bg-white/20 rounded-full h-4 mt-2 overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${((result.probability || 0) * 100)}%` }}
                        transition={{ duration: 1, ease: 'easeInOut' }}
                        className="bg-white h-full"
                      />
                    </div>
                    <p className="text-sm mt-3 font-semibold">{((result.probability || 0) * 100).toFixed(1)}%</p>
                  </div>

                  <div className="pt-6 border-t border-white/30">
                    <p className="font-semibold mb-3">💡 Recommendation</p>
                    <div className="text-white/90 leading-relaxed text-sm space-y-2">
                      {result.probability > 0.7 ? (
                        <>
                          <p>✓ Schedule immediate consultation with a doctor</p>
                          <p>✓ Get blood tests done (NS1, IgM, IgG)</p>
                          <p>✓ Rest and maintain hydration</p>
                          <p>✓ Use mosquito repellent</p>
                        </>
                      ) : result.probability > 0.4 ? (
                        <>
                          <p>✓ Monitor symptoms closely</p>
                          <p>✓ Consult with healthcare provider within 48 hours</p>
                          <p>✓ Use mosquito protection</p>
                        </>
                      ) : (
                        <>
                          <p>✓ Continue preventive measures</p>
                          <p>✓ Regular health check-ups</p>
                          <p>✓ Maintain good hygiene</p>
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
    </div>
  );
};

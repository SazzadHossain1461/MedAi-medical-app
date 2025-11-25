import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useStore } from '../../store/store';
import { toast } from 'react-toastify';
import { FiMail, FiLock, FiEye, FiEyeOff } from 'react-icons/fi';

export const Login = () => {
  const navigate = useNavigate();
  const { setUser, setIsAuthenticated } = useStore();
  
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const validateForm = () => {
    if (!formData.email || !formData.password) {
      toast.error('Please fill in all fields');
      return false;
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      toast.error('Please enter a valid email');
      return false;
    }
    if (formData.password.length < 4) {
      toast.error('Password must be at least 4 characters');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    setLoading(true);
    try {
      const userData = {
        id: Math.random().toString(36).substr(2, 9),
        email: formData.email,
        name: formData.email.split('@')[0],
        createdAt: new Date().toISOString()
      };

      localStorage.setItem('user', JSON.stringify(userData));
      localStorage.setItem('token', 'demo-token-' + Date.now());
      localStorage.setItem('isAuthenticated', 'true');

      setUser(userData);
      setIsAuthenticated(true);

      toast.success('Login successful!');
      navigate('/');
    } catch (error) {
      toast.error('Login failed. Please try again.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = (e) => {
    e.preventDefault();
    setFormData({
      email: 'demo@medai.com',
      password: 'demo123'
    });
    setTimeout(() => {
      const form = document.querySelector('form');
      if (form) form.dispatchEvent(new Event('submit', { bubbles: true }));
    }, 100);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-pink-500 to-red-500 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="w-full max-w-md"
      >
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 shadow-2xl">
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-gradient-to-br from-purple-400 to-pink-600 rounded-xl flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl font-bold text-white">M</span>
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">MedAi</h1>
            <p className="text-purple-200">Login to your account</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-white font-semibold mb-3">Email Address</label>
              <div className="relative">
                <FiMail className="absolute left-3 top-3 text-purple-300" size={20} />
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="w-full pl-10 pr-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                  placeholder="your@email.com"
                />
              </div>
            </div>

            <div>
              <label className="block text-white font-semibold mb-3">Password</label>
              <div className="relative">
                <FiLock className="absolute left-3 top-3 text-purple-300" size={20} />
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  className="w-full pl-10 pr-10 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-3 text-purple-300 hover:text-white transition-colors"
                >
                  {showPassword ? <FiEyeOff size={20} /> : <FiEye size={20} />}
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="w-4 h-4 rounded accent-purple-400" />
                <span className="text-white/80 text-sm">Remember me</span>
              </label>
              <Link to="/forgot-password" className="text-purple-200 hover:text-white text-sm transition-colors">
                Forgot password?
              </Link>
            </div>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-purple-500 to-pink-600 text-white font-bold rounded-lg hover:shadow-lg transition-all disabled:opacity-50 mt-8"
            >
              {loading ? 'Logging in...' : 'Login'}
            </motion.button>
          </form>

          <div className="my-6 flex items-center gap-4">
            <div className="flex-1 h-px bg-white/20"></div>
            <span className="text-white/60 text-sm">OR</span>
            <div className="flex-1 h-px bg-white/20"></div>
          </div>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleDemoLogin}
            className="w-full py-3 bg-white/10 border border-white/30 text-white font-semibold rounded-lg hover:bg-white/20 transition-all"
          >
            Try Demo Account
          </motion.button>

          <p className="text-center text-white/80 mt-8">
            Don't have an account?{' '}
            <Link to="/signup" className="text-purple-200 hover:text-white font-semibold transition-colors">
              Sign up
            </Link>
          </p>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mt-6 bg-white/10 backdrop-blur-md rounded-xl p-4 border border-white/20"
        >
          <p className="text-white/70 text-xs mb-2">Demo Credentials:</p>
          <p className="text-white text-sm font-mono">Email: demo@medai.com</p>
          <p className="text-white text-sm font-mono">Password: demo123</p>
        </motion.div>
      </motion.div>
    </div>
  );
};

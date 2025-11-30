import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useStore } from '../../store/store';
import { toast } from 'react-toastify';
import { FiUser, FiMail, FiLock, FiPhone, FiEye, FiEyeOff } from 'react-icons/fi';
import { FaGoogle } from 'react-icons/fa';
import { 
  createUserWithEmailAndPassword, 
  signInWithPopup 
} from 'firebase/auth';
import { auth, googleProvider } from '../../config/firebase';

export const Signup = () => {
  const navigate = useNavigate();
  const { setUser, setIsAuthenticated } = useStore();
  
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    age: '',
    gender: ''
  });

  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const validateForm = () => {
    if (!formData.fullName || !formData.email || !formData.phone || !formData.password || !formData.confirmPassword || !formData.age || !formData.gender) {
      toast.error('Please fill in all fields');
      return false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      toast.error('Please enter a valid email');
      return false;
    }

    if (formData.password.length < 6) {
      toast.error('Password must be at least 6 characters');
      return false;
    }

    if (formData.password !== formData.confirmPassword) {
      toast.error('Passwords do not match');
      return false;
    }

    if (formData.age < 18 || formData.age > 120) {
      toast.error('Please enter a valid age (18-120)');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    setLoading(true);
    try {
      const userCredential = await createUserWithEmailAndPassword(
        auth,
        formData.email,
        formData.password
      );

      const user = userCredential.user;

      const userData = {
        id: user.uid,
        fullName: formData.fullName,
        email: formData.email,
        phone: formData.phone,
        age: formData.age,
        gender: formData.gender,
        createdAt: new Date().toISOString(),
        provider: 'email'
      };

      localStorage.setItem('user', JSON.stringify(userData));
      localStorage.setItem('token', user.accessToken);
      localStorage.setItem('isAuthenticated', 'true');

      setUser(userData);
      setIsAuthenticated(true);

      toast.success('Account created successfully!');
      navigate('/');
    } catch (error) {
      console.error('Signup error:', error);
      if (error.code === 'auth/email-already-in-use') {
        toast.error('Email already in use');
      } else if (error.code === 'auth/weak-password') {
        toast.error('Password is too weak');
      } else {
        toast.error(error.message || 'Signup failed');
      }
    } finally {
      setLoading(false);
    }
  };

  // ===== GMAIL SIGNUP HANDLER =====
  const handleGoogleSignup = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      console.log('Starting Google signup...');
      
      const result = await signInWithPopup(auth, googleProvider);
      const user = result.user;

      console.log('Google user:', user);

      const userData = {
        id: user.uid,
        fullName: user.displayName || 'User',
        email: user.email,
        phone: '',
        age: '',
        gender: '',
        profileImage: user.photoURL || '',
        createdAt: new Date().toISOString(),
        provider: 'google'
      };

      localStorage.setItem('user', JSON.stringify(userData));
      localStorage.setItem('token', user.accessToken);
      localStorage.setItem('isAuthenticated', 'true');

      setUser(userData);
      setIsAuthenticated(true);

      toast.success('Signed up with Google successfully!');
      navigate('/');
    } catch (error) {
      console.error('Google signup error code:', error.code);
      console.error('Google signup error message:', error.message);
      console.error('Full error:', error);
      
      // Detailed error handling
      if (error.code === 'auth/popup-closed-by-user') {
        toast.error('Popup closed. Please try again.');
      } else if (error.code === 'auth/popup-blocked') {
        toast.error('Popup blocked by browser. Enable popups and try again.');
      } else if (error.code === 'auth/operation-not-supported-in-this-environment') {
        toast.error('Google Sign-In not supported in this environment');
      } else if (error.code === 'auth/unauthorized-domain') {
        toast.error('This domain is not authorized. Check Firebase settings.');
      } else if (error.code === 'auth/invalid-api-key') {
        toast.error('Invalid API key. Check Firebase configuration.');
      } else {
        toast.error(`Error: ${error.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-600 via-purple-500 to-pink-500 flex items-center justify-center p-4 pt-20 pb-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="w-full max-w-2xl"
      >
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 shadow-2xl">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-white mb-2">Create Account</h1>
            <p className="text-purple-200">Join MedAi to get health predictions</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-white font-semibold mb-2">Full Name</label>
                <div className="relative">
                  <FiUser className="absolute left-3 top-3 text-purple-300" size={20} />
                  <input
                    type="text"
                    name="fullName"
                    value={formData.fullName}
                    onChange={handleInputChange}
                    className="w-full pl-10 pr-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="John Doe"
                  />
                </div>
              </div>

              <div>
                <label className="block text-white font-semibold mb-2">Email Address</label>
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
                <label className="block text-white font-semibold mb-2">Phone Number</label>
                <div className="relative">
                  <FiPhone className="absolute left-3 top-3 text-purple-300" size={20} />
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    className="w-full pl-10 pr-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="+880 1234567890"
                  />
                </div>
              </div>

              <div>
                <label className="block text-white font-semibold mb-2">Age</label>
                <input
                  type="number"
                  name="age"
                  value={formData.age}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                  placeholder="25"
                  min="18"
                  max="120"
                />
              </div>

              <div>
                <label className="block text-white font-semibold mb-2">Gender</label>
                <select
                  name="gender"
                  value={formData.gender}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                >
                  <option value="">Select Gender</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div>
                <label className="block text-white font-semibold mb-2">Password</label>
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

              <div className="md:col-span-2">
                <label className="block text-white font-semibold mb-2">Confirm Password</label>
                <div className="relative">
                  <FiLock className="absolute left-3 top-3 text-purple-300" size={20} />
                  <input
                    type={showConfirmPassword ? 'text' : 'password'}
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    className="w-full pl-10 pr-10 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/60 transition-all"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-3 text-purple-300 hover:text-white transition-colors"
                  >
                    {showConfirmPassword ? <FiEyeOff size={20} /> : <FiEye size={20} />}
                  </button>
                </div>
              </div>
            </div>

            <label className="flex items-center gap-3 cursor-pointer">
              <input type="checkbox" className="w-4 h-4 rounded accent-purple-400" defaultChecked />
              <span className="text-white/80 text-sm">
                I agree to the Terms of Service and Privacy Policy
              </span>
            </label>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-bold rounded-lg hover:shadow-lg transition-all disabled:opacity-50 mt-8"
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </motion.button>
          </form>

          {/* ===== OR DIVIDER ===== */}
          <div className="my-6 flex items-center gap-4">
            <div className="flex-1 h-px bg-white/20"></div>
            <span className="text-white/60 text-sm">OR</span>
            <div className="flex-1 h-px bg-white/20"></div>
          </div>

          {/* ===== GOOGLE SIGNUP BUTTON ===== */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleGoogleSignup}
            disabled={loading}
            type="button"
            className="w-full py-3 bg-white/20 border-2 border-white/30 text-white font-semibold rounded-lg hover:bg-white/30 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
          >
            <FaGoogle size={20} />
            {loading ? 'Signing up...' : 'Sign up with Google'}
          </motion.button>

          <p className="text-center text-white/80 mt-8">
            Already have an account?{' '}
            <Link to="/login" className="text-purple-200 hover:text-white font-semibold transition-colors">
              Login
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
};
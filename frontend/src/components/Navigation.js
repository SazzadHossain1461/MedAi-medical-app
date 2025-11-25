import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { FiMenu, FiX, FiLogOut, FiHistory } from 'react-icons/fi';
import { useStore } from '../store/store';
import { LanguageSwitcher } from './LanguageSwitcher';

export const Navigation = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { isAuthenticated, user, logout } = useStore();
  const [isOpen, setIsOpen] = useState(false);

  const navLinks = [
    { path: '/', label: t('nav.home') },
    ...(isAuthenticated ? [
      { path: '/dengue', label: t('nav.dengue') },
      { path: '/kidney', label: t('nav.kidney') },
      { path: '/mental', label: t('nav.mental') },
      { path: '/history', label: 'History' }
    ] : [])
  ];

  const handleLogout = () => {
    logout();
    navigate('/login');
    setIsOpen(false);
  };

  return (
    <nav className="fixed top-0 w-full z-50 bg-gradient-to-r from-purple-600/90 to-pink-600/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center font-bold text-purple-600">
              M
            </div>
            <span className="text-white font-bold hidden sm:inline text-lg">MedAi</span>
          </Link>

          <div className="hidden md:flex items-center gap-8">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className="text-white hover:text-purple-200 transition-colors font-medium"
              >
                {link.label}
              </Link>
            ))}
          </div>

          <div className="hidden md:flex items-center gap-4">
            <LanguageSwitcher />
            
            {isAuthenticated ? (
              <div className="flex items-center gap-4">
                <span className="text-white text-sm">
                  Hello, {user?.fullName || user?.name}
                </span>
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 bg-red-500/20 border border-red-500/30 text-red-300 hover:bg-red-500/30 rounded-lg transition-all flex items-center gap-2"
                >
                  <FiLogOut size={18} /> Logout
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  to="/login"
                  className="px-4 py-2 text-white hover:bg-white/10 rounded-lg transition-all"
                >
                  Login
                </Link>
                <Link
                  to="/signup"
                  className="px-4 py-2 bg-white text-purple-600 hover:bg-white/90 rounded-lg font-semibold transition-all"
                >
                  Sign up
                </Link>
              </div>
            )}
          </div>

          <button
            className="md:hidden text-white"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? <FiX size={24} /> : <FiMenu size={24} />}
          </button>
        </div>

        {isOpen && (
          <div className="md:hidden bg-purple-700/95 backdrop-blur-md">
            <div className="px-2 pt-2 pb-3 space-y-1">
              {navLinks.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  className="block px-3 py-2 text-white hover:bg-purple-600 rounded-lg transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  {link.label}
                </Link>
              ))}
              <div className="px-3 py-2">
                <LanguageSwitcher />
              </div>
              {isAuthenticated ? (
                <button
                  onClick={handleLogout}
                  className="w-full text-left px-3 py-2 text-red-300 hover:bg-purple-600 rounded-lg transition-colors flex items-center gap-2"
                >
                  <FiLogOut size={18} /> Logout
                </button>
              ) : (
                <div className="flex gap-2 px-3 py-2">
                  <Link
                    to="/login"
                    className="flex-1 text-center px-3 py-2 text-white hover:bg-purple-600 rounded-lg transition-colors"
                    onClick={() => setIsOpen(false)}
                  >
                    Login
                  </Link>
                  <Link
                    to="/signup"
                    className="flex-1 text-center px-3 py-2 bg-white text-purple-600 hover:bg-white/90 rounded-lg font-semibold transition-all"
                    onClick={() => setIsOpen(false)}
                  >
                    Sign up
                  </Link>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

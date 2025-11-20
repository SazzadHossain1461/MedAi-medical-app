import React from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiArrowRight, FiHeart, FiActivity, FiUser } from 'react-icons/fi';

export const HomePage = () => {
  const { t } = useTranslation();

  const features = [
    {
      icon: FiHeart,
      title: t('nav.dengue'),
      description: t('dengue.description'),
      link: '/dengue',
      color: 'from-red-400 to-pink-600'
    },
    {
      icon: FiActivity,
      title: t('nav.kidney'),
      description: t('kidney.description'),
      link: '/kidney',
      color: 'from-blue-400 to-cyan-600'
    },
    {
      icon: FiUser, // Replaced FiBrain with FiUser (available icon)
      title: t('nav.mental'),
      description: t('mental.description'),
      link: '/mental',
      color: 'from-purple-400 to-indigo-600'
    }
  ];

  return (
    <div className="pt-20 min-h-screen bg-gradient-to-br from-purple-600 via-pink-500 to-red-500">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center text-white mb-16"
        >
          <h1 className="text-5xl md:text-7xl font-bold mb-6">
            {t('home.title')}
          </h1>
          <p className="text-xl md:text-2xl mb-4 text-purple-100">
            {t('home.subtitle')}
          </p>
          <p className="text-lg text-purple-200 mb-8 max-w-2xl mx-auto">
            {t('home.description')}
          </p>
        </motion.div>

        {/* Feature Cards */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {features.map((feature, idx) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.2 }}
                whileHover={{ y: -10 }}
                className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 hover:border-white/40 transition-all"
              >
                <div className={`w-16 h-16 rounded-lg bg-gradient-to-br ${feature.color} flex items-center justify-center mb-4`}>
                  <Icon size={32} className="text-white" />
                </div>
                <h3 className="text-2xl font-bold text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-purple-200 mb-6">
                  {feature.description}
                </p>
                <Link
                  to={feature.link}
                  className="inline-flex items-center gap-2 text-white hover:text-purple-200 transition-colors font-semibold"
                >
                  {t('common.submit')} <FiArrowRight />
                </Link>
              </motion.div>
            );
          })}
        </div>

        {/* Stats Section */}
        <div className="grid md:grid-cols-4 gap-6 mb-12">
          {[
            { label: 'Accuracy', value: '98%' },
            { label: 'Users', value: '10K+' },
            { label: 'Predictions', value: '100K+' },
            { label: 'Models', value: '3' }
          ].map((stat, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: idx * 0.1 }}
              className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20 text-center"
            >
              <div className="text-3xl font-bold text-white mb-2">{stat.value}</div>
              <div className="text-purple-200">{stat.label}</div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
};
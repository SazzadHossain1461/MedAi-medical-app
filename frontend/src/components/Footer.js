import React from 'react';
import { useTranslation } from 'react-i18next';
import { FiMail, FiPhone, FiMapPin } from 'react-icons/fi';

export const Footer = () => {
  const { t } = useTranslation();

  return (
    <footer className="bg-gradient-to-r from-purple-900 to-indigo-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* About */}
          <div>
            <h3 className="text-xl font-bold mb-4">MedAi</h3>
            <p className="text-purple-200">{t('footer.description')}</p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-purple-200">
              <li><a href="#" className="hover:text-white transition-colors">Home</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Services</a></li>
              <li><a href="#" className="hover:text-white transition-colors">About</a></li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Legal</h4>
            <ul className="space-y-2 text-purple-200">
              <li><a href="#" className="hover:text-white transition-colors">{t('footer.privacy')}</a></li>
              <li><a href="#" className="hover:text-white transition-colors">{t('footer.terms')}</a></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="text-lg font-semibold mb-4">{t('footer.contact')}</h4>
            <div className="space-y-2 text-purple-200">
              <div className="flex items-center gap-2">
                <FiMail size={18} />
                <span> sazzadhossain74274@gmail.com</span>
              </div>
              <div className="flex items-center gap-2">
                <FiPhone size={18} />
                <span>+880 1983027130</span>
              </div>
              <div className="flex items-center gap-2">
                <FiMapPin size={18} />
                <span>Dhaka, Bangladesh</span>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-purple-700 pt-8 text-center text-purple-200">
          <p>{t('footer.copyright')}</p>
        </div>
      </div>
    </footer>
  );
};
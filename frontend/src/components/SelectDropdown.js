import React, { useState, useRef, useEffect } from 'react';
import { FiChevronDown } from 'react-icons/fi';

export const SelectDropdown = ({ 
  name, 
  value, 
  onChange, 
  options, 
  label,
  required = false 
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const selectedOption = options.find(opt => opt.value === value);

  return (
    <div className="relative" ref={dropdownRef}>
      {label && (
        <label className="block text-white font-semibold mb-2">
          {label}
          {required && <span className="text-red-400">*</span>}
        </label>
      )}
      
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-4 py-3 rounded-lg bg-white/20 border-2 border-white/30 text-white hover:border-white/50 focus:outline-none focus:border-white/60 transition-all duration-200 flex items-center justify-between text-left font-medium"
      >
        <span className={selectedOption ? 'text-white' : 'text-white/70'}>
          {selectedOption ? selectedOption.label : 'Select an option'}
        </span>
        <FiChevronDown 
          size={20} 
          className={`transition-transform duration-200 ${isOpen ? 'transform rotate-180' : ''}`}
        />
      </button>

      {isOpen && (
        <div className="absolute z-50 w-full mt-2 bg-gray-900 border-2 border-white/30 rounded-lg shadow-xl overflow-hidden backdrop-blur-md">
          <div className="max-h-60 overflow-y-auto">
            {options.map((option) => (
              <button
                key={option.value}
                type="button"
                onClick={() => {
                  onChange({
                    target: {
                      name,
                      value: option.value
                    }
                  });
                  setIsOpen(false);
                }}
                className={`w-full px-4 py-3 text-left transition-colors duration-150 font-medium ${
                  value === option.value
                    ? 'bg-blue-500/50 text-white border-l-4 border-blue-400'
                    : 'text-white/90 hover:bg-white/10 border-l-4 border-transparent'
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

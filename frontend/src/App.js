import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './i18n/i18n';

import { Navigation } from './components/Navigation';
import { HomePage } from './components/HomePage';
import { DenguePrediction } from './components/DenguePrediction';
import { KidneyPrediction } from './components/KidneyPrediction';
import { MentalHealthAssessment } from './components/MentalHealthAssessment';
import { Footer } from './components/Footer';

function App() {
  return (
    <Router>
      <div className="w-full min-h-screen flex flex-col bg-gradient-to-br from-purple-600 to-indigo-600">
        <Navigation />
        <main className="flex-grow w-full">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/dengue" element={<DenguePrediction />} />
            <Route path="/kidney" element={<KidneyPrediction />} />
            <Route path="/mental" element={<MentalHealthAssessment />} />
          </Routes>
        </main>
        <Footer />
        <ToastContainer
          position="bottom-right"
          autoClose={3000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="dark"
        />
      </div>
    </Router>
  );
}

export default App;
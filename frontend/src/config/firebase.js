// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDnxKER789xrAobgzAv53I0ZGzK5vIVITs",
  authDomain: "medai-be9d7.firebaseapp.com",
  projectId: "medai-be9d7",
  storageBucket: "medai-be9d7.firebasestorage.app",
  messagingSenderId: "117018885498",
  appId: "1:117018885498:web:58eeb53c97f3f6ac4d2ac3",
  measurementId: "G-72Z9E4N38S"
};

// Initialize Firebase
let app;
let auth;
let googleProvider;

try {
  app = initializeApp(firebaseConfig);
  console.log('✅ Firebase initialized successfully');
  
  // Initialize Analytics
  const analytics = getAnalytics(app);
  console.log('✅ Analytics initialized');
  
  // Initialize Auth
  auth = getAuth(app);
  console.log('✅ Auth initialized');
  
  // Configure Google Provider
  googleProvider = new GoogleAuthProvider();
  googleProvider.addScope('profile');
  googleProvider.addScope('email');
  console.log('✅ Google Provider configured');
  
} catch (error) {
  console.error('❌ Firebase initialization error:', error);
}

export { app, auth, googleProvider };
export default app;
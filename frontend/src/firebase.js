// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";

import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDzghXVTjA1R_ggHbeFUYBOORGSw7KmTcM",
  authDomain: "booking-ai-agent-a5c95.firebaseapp.com",
  projectId: "booking-ai-agent-a5c95",
  storageBucket: "booking-ai-agent-a5c95.firebasestorage.app",
  messagingSenderId: "110717061081",
  appId: "1:110717061081:web:619e9f37d48b430f457bc8",
  measurementId: "G-YPZT4QBR2F"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
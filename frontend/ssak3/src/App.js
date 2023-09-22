// import React, { useState } from "react";
// import TurtlebotController from "./components/turtlebotcontroller/index.jsx";
import './App.css';
import TurtlebotStarter from "./components/turtlebotstarter/index.jsx";
import SignUp from './pages/Auth/SignUp';
import Login from "./pages/LogIn.jsx";

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  return (
  <>
    <Router>
      <Routes>
        <Route path="/" element={<TurtlebotStarter/>} />
        <Route path="login" element={<Login/>} />
        <Route path="signup" element={<SignUp/>} />
      </Routes>
    </Router>
  </>
  );
}

export default App;

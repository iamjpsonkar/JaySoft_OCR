// Layout.js
import React from 'react';
import Header from '../Header/Header';
import Footer from '../Footer/Footer';
import Home from '../Home/Home';
// import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';

const Layout = ({ children }) => {
    return (
        <div>
            <Header />
            <Home/>
            <Footer />
        </div>
    );
};

export default Layout;

// Layout.js
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from '../Header/Header';
import Footer from '../Footer/Footer';
import Home from '../Home/Home';
import ImageUpload from '../ImageUpload/ImageUpload';
import OcrResult from '../OcrResult/OcrResult';
// import Contact from '../Contact/Contact';

const Layout = () => {
    return (
        <div>
            <Header />
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="upload/image" element={<ImageUpload />} />
                {/* <Route path="/ocr/result" element={<OcrResult />} /> */}
                <Route
                    path="/ocr/result"
                    element={<OcrResult />}
                />
            </Routes>
            <div className='content'></div>
            <Footer />
        </div>
    );
};

export default Layout;

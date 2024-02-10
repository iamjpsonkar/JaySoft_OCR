import React from 'react';
import logo from './assets/images/logo.png';

const Header = () => {
    return (
        <div className="container-fluid header">
            <div className="row d-flex align-items-center">
                <div className="col-sm-7">
                    <a href="/" className="normal-link">
                        <h1>
                            <img style={{ padding: '2px' }} src={logo} alt="logo" />
                            JaySoft-OCR
                        </h1>
                    </a>
                </div>
                <div className="col-sm-5">
                    <div className="d-flex align-items-center" style={{ padding: '3%' }}>
                        <p className="text-center">
                            <i>
                                "Get text from pictures easily. Our app makes it simple to extract words from images."
                            </i>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Header;
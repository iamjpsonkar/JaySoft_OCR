import React from 'react';
import { useLocation } from 'react-router-dom';
import ReactJson from 'react-json-view';

const OcrResult = () => {
    // Access the OCR result data from location state
    const location = useLocation();
    const { resultData } = location.state || {};

    return ( 
    
        <div>
            <h2 className="mb-4 text-center">OCR Result</h2>
            {/* Display the OCR result data */}
            {resultData && (
                <div>
                    <ReactJson src={resultData} collapsed={1} />
                </div>
            )}
        </div>
    );
};

export default OcrResult;
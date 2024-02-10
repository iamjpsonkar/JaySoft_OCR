import React from 'react';
import { useLocation } from 'react-router-dom';

const OcrResult = () => {
    // Access the OCR result data from location state
    const location = useLocation();
    const { resultData } = location.state || {};

    return (
        <div className="text-center">
            <h2 className="mb-4">OCR Result</h2>
            {/* Display the OCR result data */}
            <p>OCR Result: {resultData && resultData.message}</p>
        </div>
    );
};

export default OcrResult;
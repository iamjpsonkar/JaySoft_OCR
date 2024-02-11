import React from 'react';
import { useLocation } from 'react-router-dom';
import ReactJson from 'react-json-view';

const OcrResult = () => {
    // Access the OCR result data from location state
    const location = useLocation();
    const response_data = location?.state?.resultData?.response_data || {};
    const image = location?.state?.resultData?.image || "";

    // Function to decode base64 image
    const decodeBase64Image = (base64Image) => {
        return `data:image/jpeg;base64,${base64Image}`;
    };

    // Log image and response_data for debugging
    console.log("image:", image);
    console.log("response_data:", response_data);

    return (
        <div className="container"  style={{ marginBottom: '100px' }}>
            <h2  className="mb-4 text-center"><a style={{ margin: '1px' }}className="btn btn-primary" href="../upload/image">
                Upload Another Image
            </a><a style={{ margin: '1px' }} className="btn btn-primary" href="../images">
                View All Images
            </a></h2>
            <h2 className="mb-4 text-center">OCR Result</h2>
            <div className="row">
                <div className="col-md-6">
                    {/* Display the image */}
                    {image ? (
                        <img src={decodeBase64Image(image)} alt="OCR Image" style={{ maxWidth: '100%', height: 'auto' }} />
                    ) : (
                        <p>No image found.</p>
                    )}
                </div>
                <div className="col-md-6">
                    {/* Display the OCR result data */}
                    {response_data && Object.keys(response_data).length > 0 ? (
                        <ReactJson src={response_data} collapsed={1} />
                    ) : (
                        <p>No OCR result data found.</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default OcrResult;

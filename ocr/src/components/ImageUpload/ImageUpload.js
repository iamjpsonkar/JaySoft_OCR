import axios from 'axios';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Config from '../../Config';

const ImageUpload = () => {
    const [file, setFile] = useState(null);
    const [validFile, setValidFile] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [showUploadingMessage, setShowUploadingMessage] = useState(false); // State to control the visibility of the uploading message
    const navigate = useNavigate();

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile && selectedFile.type.startsWith('image/')) {
            setFile(selectedFile);
            setValidFile(true);
        } else {
            setFile(null);
            setValidFile(false);
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!file) return;

        try {
            setShowUploadingMessage(true); // Show the uploading message
            setUploading(true); // Set uploading to true before starting the upload

            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = async () => {
                const base64Image = reader.result.split(',')[1];

                const response = await axios.post(Config.backend_server + '/process/image', {
                    image: base64Image,
                    imageName: file.name,
                    imageType: file.type
                }, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                console.log('Response:', response.data);

                if (response.status === 200) {
                    navigate('/ocr/result', { state: { resultData: response.data } });
                }
            };
        } catch (error) {
            console.error('Error uploading image:', error);
        } finally {
            setUploading(false); // Set uploading to false after finishing the upload
        }
    };

    return (
        <div className="text-center">
            <h2 className="mb-4">Upload Image</h2>
            <form onSubmit={handleSubmit} encType="multipart/form-data">
                <div className="form-group">
                    <label htmlFor="image">Choose Image:</label>
                    <input type="file" className="form-control-file" id="image" name="image" onChange={handleFileChange} />
                </div>
                {validFile && (
                    <>
                        <button type="submit" className="btn btn-primary" disabled={uploading}>
                            {uploading ? 'Uploading... Please wait' : 'Upload'}
                        </button>
                        {showUploadingMessage && (
                            <div className="alert alert-info ml-2" role="alert">
                                Processing for OCR... Please wait.
                            </div>
                        )}
                    </>
                )}
                {!validFile && (
                    <span className="text-danger">Please select a valid image file.</span>
                )}
            </form>
        </div>
    );
};

export default ImageUpload;

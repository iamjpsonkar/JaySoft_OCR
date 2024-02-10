import axios from 'axios';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate hook
import Config from '../../Config';

const ImageUpload = () => {
    const [file, setFile] = useState(null);
    const navigate = useNavigate(); // Initialize useNavigate hook

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        
        try {
            // Read the selected file and convert it to base64 string
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = async () => {
                const base64Image = reader.result.split(',')[1]; // Extract base64 string from data URL

                // Send the base64 image string to the backend
                const response = await axios.post(Config.backend_server + '/process/image', { image: base64Image }, {
                    headers: {
                        'Content-Type': '*/*'
                    }
                });

                console.log('Response:', response.data);

                if (response.status === 200) {
                    // Redirect to OCR result page
                    navigate('/ocr/result', { state: { resultData: response.data } });
                }
            };
        } catch (error) {
            console.error('Error uploading image:', error);
        }
    };

    return (
        <div className="text-center">
            <h2 className="mb-4">Upload Image</h2>
            <form onSubmit={handleSubmit} encType="multipart/form-data">
                <div className="form-group">
                    <label htmlFor="image" style={{ margin:"1em" }}>Choose Image:</label>
                    <input type="file" className="form-control-file" id="image" name="image" onChange={handleFileChange} style={{ margin:"1em" }} />
                </div>
                <button type="submit" className="btn btn-primary" style={{ margin:"1em" }}>Upload</button>
            </form>
        </div>
    );
};

export default ImageUpload;

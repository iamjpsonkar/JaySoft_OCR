import axios from 'axios';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Config from '../../Config';

const ImageUpload = () => {
    const [file, setFile] = useState(null);
    const navigate = useNavigate();

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        
        try {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = async () => {
                const base64Image = reader.result.split(',')[1];

                const response = await axios.post(Config.backend_server + '/process/image', {
                    image: base64Image,
                    imageName: file.name, // Fetching image name from the file object
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
                <button type="submit" className="btn btn-primary">Upload</button>
            </form>
        </div>
    );
};

export default ImageUpload;

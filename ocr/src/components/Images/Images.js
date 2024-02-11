import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Config from '../../Config';
import { useNavigate } from 'react-router-dom'; // Import useNavigate instead of useHistory

const Images = () => {
    const [images, setImages] = useState([]);
    const [selectedImage, setSelectedImage] = useState(null);
    const [ocrResult, setOcrResult] = useState('');
    const navigate = useNavigate(); // Use useNavigate instead of useHistory

    useEffect(() => {
        // Fetch images from backend API
        fetchImages();
    }, []);

    const fetchImages = async () => {
        try {
            const response = await axios.get(Config.backend_server + '/images');
            setImages(response.data);
        } catch (error) {
            console.error('Error fetching images:', error);
        }
    };

    const handleImageClick = async (imageId, base64Image, imageName, imageType) => {
        try {
            const response = await axios.post(Config.backend_server + '/process/image', {
                image_id: imageId,
                image: base64Image,
                imageName: imageName,
                imageType: imageType
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            console.log('Response:', response.data);

            if (response.status === 200) {
                setSelectedImage(imageId); // Update selectedImage state
                navigate('/ocr/result', { state: { resultData: response.data } }); // Use navigate for navigation
            }
        } catch (error) {
            console.error('Error processing image:', error);
        }
    };

    return (
        <div>
            <h1>Images <a style={{ margin: '1px' }} className="btn btn-primary" href="../">
                Back to Home
            </a></h1>
            <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(4, 1fr)', 
                gap: '20px',
                padding: '20px',
                marginBottom: '100px'
            }}>
                {images.map((image) => (
                    <div 
                        key={image.image_id}
                        style={{
                            border: '1px solid #ccc',
                            borderRadius: '5px',
                            padding: '10px',
                            backgroundColor: selectedImage === image.image_id ? '#f0f0f0' : '#ffffff',
                        }}
                    >
                        <img
                            src={`data:image/jpeg;base64,${image.base64html}`}
                            alt={image.image_name}
                            onClick={() => handleImageClick(image.image_id, image.base64html, image.image_name, 'image/jpeg')}
                            style={{ cursor: 'pointer', maxWidth: '100%', height: 'auto' }}
                        />
                        <div style={{ marginTop: '10px' }}>
                            <a
                                href="#"
                                onClick={() => handleImageClick(image.image_id, image.base64html, image.image_name, 'image/jpeg')}
                                style={{ display: 'block' }}
                            >
                                {image.image_name}
                            </a>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Images;

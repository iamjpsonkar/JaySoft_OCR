import React from 'react';

const Home = () => {
    return (
        <div>
            <div className="d-flex flex-column align-items-center" style={{ padding: '10%' }}>
                <p className="text-center">
                    <i>
                        "Our simple OCR web app quickly reads text from images. Just upload your picture, and our advanced technology does the rest. Whether it's printed documents, images with text, or scanned files, our app handles it all effortlessly. No more manual typing or data entry—our powerful OCR engine ensures accurate and reliable results every time. Say goodbye to tedious tasks and hello to streamlined document processing. With our user-friendly platform, digitizing text has never been easier. Experience the convenience of our OCR web app today!"
                    </i>
                </p>
                <a className="btn btn-primary" href="upload/image">
                    Upload Image
                </a>
            </div>
        </div>
    );
};

export default Home;
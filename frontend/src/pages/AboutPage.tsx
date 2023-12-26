import React from 'react';
import logo from '../logo.svg';

const AboutPage: React.FC = () => {
    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                <p>
                    About
                </p>
            </header>
        </div>
    )
};

export default AboutPage;

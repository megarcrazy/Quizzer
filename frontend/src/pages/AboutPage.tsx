import React from 'react';
import NavigationBar from '../components/NavigationBar';
import logo from '../logo.svg';

const AboutPage: React.FC = () => {
    return (
        <div className="App">
            <NavigationBar />
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

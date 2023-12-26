import React from 'react';
import logo from '../logo.svg';

const HomePage: React.FC = () => {
    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                <p>
                    Home
                </p>
            </header>
        </div>
    )
};

export default HomePage;

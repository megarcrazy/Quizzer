import React from 'react';
import logo from '../logo.svg';

const ErrorPage: React.FC = () => {
    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                <p>
                    Oops! This link does not exist. Please go back to home.
                </p>
            </header>
        </div>
    )
};

export default ErrorPage;

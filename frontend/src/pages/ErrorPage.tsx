import React from 'react';
import NavigationBar from '../components/NavigationBar';
import logo from '../logo.svg';

const ErrorPage: React.FC = () => {
    return (
        <div className="App">
            <NavigationBar />
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

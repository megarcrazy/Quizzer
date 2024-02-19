import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../logo.svg';

const HomePage: React.FC = () => {
    const navigate = useNavigate();

    useEffect(() => {
        // Redirect to '/home' when the component mounts
        navigate('/home');
    }, [navigate]);

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

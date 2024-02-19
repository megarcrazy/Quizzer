import React from 'react';
import NavigationBar from '../components/NavigationBar';
import logo from '../logo.svg';

const EditSavedQuizPage: React.FC = () => {
    return (
        <div className="App">
            <NavigationBar />
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                <p>
                    Edit
                </p>
            </header>
        </div>
    )
};

export default EditSavedQuizPage;

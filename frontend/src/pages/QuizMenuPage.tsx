import React from 'react';
import logo from '../logo.svg';

const QuizMenuPage: React.FC = () => {
    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                <p>
                    My Quizzes
                </p>
            </header>
        </div>
    )
};

export default QuizMenuPage;

import './App.css';
import { Routes, Route, BrowserRouter as Router } from 'react-router-dom';
// Pages
import HomePage from './pages/HomePage';
import QuizMenuPage from './pages/QuizMenuPage';
import PlaySavedQuizPage from './pages/PlaySavedQuizPage';
import EditSavedQuizPage from './pages/EditSavedQuizPage';
import AboutPage from './pages/AboutPage';
import ErrorPage from './pages/ErrorPage';


function App() {
  return (
    <Router>
      {/* The Routes component is used to define different routes */}
      <Routes>
        <Route path='/' element={<HomePage />} />
        <Route path='/home' element={<HomePage />} />
        <Route path='/my-quizzes' element={<QuizMenuPage />} />
        <Route path='/play' element={<PlaySavedQuizPage />} />
        <Route path='/edit' element={<EditSavedQuizPage />} />
        <Route path='/about' element={<AboutPage />} />
        <Route path="*" element={<ErrorPage />} />
      </Routes>
    </Router>
  );
}

export default App;

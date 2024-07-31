import React from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoadingBar from 'react-top-loading-bar';
import ScrollToTop from './ScrollToTop';

import Navbar from './components/Navbar/Navbar';
import Footer from './components/Footer/Footer';

import Home from './pages/Home';
import FullTimetable from './pages/FullTimetable';
import Dashboard from './pages/Dashboard';

function App() {

    const [title, setTitle] = React.useState('ClassGrid by DevClub - Your Semester Timetable in 2 Minutes');
    const [progress, setProgress] = React.useState(0);
    const [msFailAlert, setMsFailAlert] = React.useState(true);

    React.useEffect(() => {
        document.title = title;
    }, [title]);

    React.useEffect(() => {
        if (msFailAlert) {
            alert("IMPORTANT: CSC, IIT Delhi servers are facing some issue with Microsoft in their authentication flow. Due to this, you might not be able to log in to ClassGrid. Please check back later. [Last Updated: 13:08, 31 July 2024 (IST)]");
            setMsFailAlert(false);
        }
    }, [msFailAlert])

    return (
        <BrowserRouter>
            <LoadingBar
                color='#EF5B5B'
                progress={progress}
                onLoaderFinished={() => setProgress(0)}
            />
            <ScrollToTop />
            <header>
                <Navbar />
            </header>
            <main>
                <Routes>
                    <Route path="/" element={<Home setProgress={setProgress} setTitle={setTitle} />} />
                    <Route path="/dashboard" element={<Dashboard setProgress={setProgress} setTitle={setTitle} />} />
                    <Route path="/timetable" element={<FullTimetable setProgress={setProgress} setTitle={setTitle} />} />
                </Routes>
            </main>
            <footer>
                <Footer />
            </footer>
        </BrowserRouter>
    );
}

export default App;

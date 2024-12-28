import React from 'react'
import './Home.css'
import hero from '../../assets/hero.png'
import { Link, useNavigate } from 'react-router-dom';

import { useMsal } from "@azure/msal-react";
import { loginRequest } from '../../authConfig';

export default function HomeComp() {

    const { instance, accounts } = useMsal();
    const navigate = useNavigate();

    const handleLogin = () => {
        instance.loginRedirect(loginRequest).catch(e => {
            console.log(e);
        });
    }

    React.useEffect(() => {
        if (accounts.length > 0) {
            navigate('/dashboard');
        }

    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [accounts])

    return (
        <section>
            <div className="home">
                <div className="home-content">
                    <h2>
                        Your Semester Timetable in 2 Minutes.
                    </h2>
                    <p>
                        With ClassGrid, you can prepare the timetable of your entire semester in 2 minutes. Key features include:
                        <ul>
                            <li>Accounts for holidays and substitution days</li>
                            <li>Customise Tutorials and Labs as per your choice</li>
                            <li>T-10 reminders and Room Numbers for Lectures and Tutorials</li>
                        </ul>    
                    </p>
                    <p>Please note that ClassGrid may not behave correctly for UG First Year courses. For any other issues you face while using ClassGrid, fill out <Link to="https://forms.gle/zadVEANZhCYS6gkv5" target='_blank'>this form</Link>.</p>
                    <button onClick={handleLogin}>
                        Get Started
                    </button>
                </div>
                <div className="home-hero">
                    <img src={hero} alt="ClassGrid" />
                </div>
            </div>
        </section>
    )
}

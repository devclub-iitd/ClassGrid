import React from 'react'
import './Home.css'
import hero from '../../assets/hero.png'
import { useNavigate } from 'react-router-dom';

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
                    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime corporis et, magni laboriosam perferendis dicta deserunt adipisci placeat eveniet laudantium?</p>
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

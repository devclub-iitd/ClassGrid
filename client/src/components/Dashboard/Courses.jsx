import React from 'react'
import './Dashboard.css'
import { useMsal } from '@azure/msal-react';

export default function Courses(props) {

    const name = props.name;
    const courses = props.courses;
    const setNavigation = props.setNavigation;

    const { instance } = useMsal();

    const signout = () => {
        instance.logoutRedirect({
            postLogoutRedirectUri: "/",
        });
    }

    return (
        <section className='pre-dashboard'>
            <div className="course-list">
                <h1>Hi {name} 👋</h1>
                <p>Please verify your courses for Winter Semester, 2023-24</p>
                <ul>
                    {courses.map((course, index) => {
                        return <li key={index}>{course}</li>
                    })}
                </ul>
                <button onClick={() => setNavigation(2)}>
                    Continue
                </button>
                <p className="logout">Not you? <span onClick={signout}>Sign out</span></p>
            </div>
        </section>
    )
}

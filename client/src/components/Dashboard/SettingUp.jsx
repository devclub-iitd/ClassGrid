import React from 'react'
import axios from 'axios';
import './Dashboard.css'
import { useMsal } from '@azure/msal-react';
import { loginRequest } from '../../authConfig';

export default function SettingUp(props) {

    const setNavigation = props.setNavigation;
    const setProgress = props.setProgress;
    const setName = props.setName;
    const setTimetable = props.setTimetable;
    
    const { instance, accounts } = useMsal();

    React.useEffect(() => {

        instance
            .acquireTokenSilent({
                ...loginRequest,
                account: accounts[0],
            })
            .then((response) => {
                axios.get(`https://classgrid.devclub.iitd.tech/api/timetable/`, {
                    headers: {
                        Authorization: `Bearer ${response.accessToken}`,
                    }
                })
                .then(res => {
                    setName(res.data.name);
                    setTimetable(res.data.courses);
                    setProgress(100);
                    setNavigation(3);
                })
                .catch(err => {
                    console.log(err);
                })
            })

        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    return (
        <section className='pre-dashboard'>
            <div className="fetching-courses">
                <h1>Please wait while we set up your timetable</h1>
                <div className="loading-balls">
                    <div className="loading-ball"></div>
                    <div className="loading-ball"></div>
                    <div className="loading-ball"></div>
                </div>
            </div>
        </section>
    )
}

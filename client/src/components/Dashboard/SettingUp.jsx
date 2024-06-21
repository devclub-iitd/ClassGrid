import React from 'react'
import axios from 'axios';
import './Dashboard.css'

export default function SettingUp(props) {

    const setNavigation = props.setNavigation;
    const setProgress = props.setProgress;
    const kerberos = props.kerberos;
    const setName = props.setName;
    const setTimetable = props.setTimetable;

    React.useEffect(() => {
        axios.get(`http://localhost:8000/api/timetable?kerberos=${kerberos}`)
            .then(res => {
                setName(res.data.name);
                setTimetable(res.data.courses);
                setProgress(100);
                setNavigation(3);
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

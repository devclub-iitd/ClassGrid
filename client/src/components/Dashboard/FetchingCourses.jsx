import React from 'react'
import axios from 'axios';
import './Dashboard.css'

export default function FetchingCourses(props) {

    const setNavigation = props.setNavigation;
    const setProgress = props.setProgress;
    const kerberos = props.kerberos;
    const setName = props.setName;
    const setCourses = props.setCourses;

    React.useEffect(() => {
        axios.get(`https://classgrid.devclub.iitd.tech/api/courses?kerberos=${kerberos}`)
            .then(res => {
                setName(res.data.name);
                setCourses(res.data.courses);
                setProgress(100);
                setNavigation(1);
            })

        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    return (
        <section className='pre-dashboard'>
            <div className="fetching-courses">
                <h1>Fetching your courses</h1>
                <div className="loading-balls">
                    <div className="loading-ball"></div>
                    <div className="loading-ball"></div>
                    <div className="loading-ball"></div>
                </div>
            </div>
        </section>
    )
}

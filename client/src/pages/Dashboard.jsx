import React from 'react'
import FetchingCourses from '../components/Dashboard/FetchingCourses';
import Courses from '../components/Dashboard/Courses';
import { Navigate } from 'react-router-dom';
import Timetable from '../components/Dashboard/Timetable';
import SettingUp from '../components/Dashboard/SettingUp';

import { AuthenticatedTemplate, UnauthenticatedTemplate } from '@azure/msal-react';

export default function Dashboard(props) {

    const setTitle = props.setTitle;
    const setProgress = props.setProgress;

    React.useEffect(() => {
        setTitle("My Dashboard | ClassGrid by DevClub IIT Delhi")
        setProgress(25);

    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    const [navigation, setNavigation] = React.useState(0);
    const [name, setName] = React.useState();
    const [courses, setCourses] = React.useState([]);
    const [timetable, setTimetable] = React.useState({});

    return (
        <>
            <AuthenticatedTemplate>
                {navigation === 0 ? <FetchingCourses setName={setName} setCourses={setCourses} setNavigation={setNavigation} setProgress={setProgress} /> : null}
                {navigation === 1 ? <Courses name={name} courses={courses} setNavigation={setNavigation} /> : null}
                {navigation === 2 ? <SettingUp setName={setName} setTimetable={setTimetable} setNavigation={setNavigation} setProgress={setProgress} /> : null}
                {navigation === 3 ? <Timetable name={name} timetable={timetable} setNavigation={setNavigation} /> : null}
            </AuthenticatedTemplate>

            <UnauthenticatedTemplate>
                <Navigate to="/" />
            </UnauthenticatedTemplate>
        </>
    )
}

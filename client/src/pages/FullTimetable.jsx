import React from 'react'
import { Navigate } from 'react-router-dom';
import Timetable from '../components/FullTimetable/Timetable';
import SettingUp from '../components/FullTimetable/SettingUp';

import { AuthenticatedTemplate, UnauthenticatedTemplate } from '@azure/msal-react';

export default function FullTimetable(props) {

    const setTitle = props.setTitle;
    const setProgress = props.setProgress;

    React.useEffect(() => {
        setTitle("Full Timetable | ClassGrid by DevClub IIT Delhi")
        setProgress(25);

    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    const [navigation, setNavigation] = React.useState(0);
    const [name, setName] = React.useState();
    const [timetable, setTimetable] = React.useState({});

    return (
        <>
            <AuthenticatedTemplate>
                {navigation === 0 ? <SettingUp setName={setName} setTimetable={setTimetable} setNavigation={setNavigation} setProgress={setProgress} /> : null}
                {navigation === 1 ? <Timetable name={name} timetable={timetable} setNavigation={setNavigation} /> : null}
            </AuthenticatedTemplate>

            <UnauthenticatedTemplate>
                <Navigate to="/" />
            </UnauthenticatedTemplate>
        </>
    )
}

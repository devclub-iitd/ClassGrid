import React from 'react'
import { Navigate } from 'react-router-dom';
import DashboardComp from '../components/Dashboard/Dashboard'

import { AuthenticatedTemplate, UnauthenticatedTemplate } from '@azure/msal-react';

export default function Dashboard(props) {

    const setTitle = props.setTitle;
    const setProgress = props.setProgress;

    React.useEffect(() => {
        setTitle("My Dashboard | ClassGrid by DevClub IIT Delhi")
        setProgress(25);

    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    return (
        <>
            <AuthenticatedTemplate>
                <DashboardComp setProgress={setProgress} />
            </AuthenticatedTemplate>

            <UnauthenticatedTemplate>
                <Navigate to="/" />
            </UnauthenticatedTemplate>
        </>
    )
}

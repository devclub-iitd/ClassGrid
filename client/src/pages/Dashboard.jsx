import React from 'react'
import { Navigate } from 'react-router-dom';
import DashboardComp from '../components/Dashboard/Dashboard'

import { AuthenticatedTemplate, UnauthenticatedTemplate } from '@azure/msal-react';

export default function Dashboard() {
    return (
        <>
            <AuthenticatedTemplate>
                <DashboardComp />
            </AuthenticatedTemplate>

            <UnauthenticatedTemplate>
                <Navigate to="/" />
            </UnauthenticatedTemplate>
        </>
    )
}

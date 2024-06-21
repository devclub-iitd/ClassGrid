import React from 'react'
import LoginForm from '../components/Signin/LoginForm';

export default function Signin(props) {

    const setTitle = props.setTitle;
    const setProgress = props.setProgress;

    React.useEffect(() => {
        setTitle("Sign In to ClassGrid | DevClub IIT Delhi")
        setProgress(100);

    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    return (
        <LoginForm />
    )
}

import React from 'react'
import './Signin.css'
import { useNavigate } from 'react-router-dom';

export default function LoginForm() {

    const navigate = useNavigate();

    function validateEntryNumber() {
        const entryNumber = document.getElementById('signin-form-entryNumber').value;
        const submitButton = document.getElementById('signin-form-submit');
        const regex = /^\d{4}[A-Za-z]{2}\d{5}$/;
        if (regex.test(entryNumber)) {
            submitButton.disabled = false;
        } else {
            submitButton.disabled = true;
        }
    }

    function handleSignIn(e) {
        e.preventDefault();
        const entryNumber = document.getElementById('signin-form-entryNumber').value;
        const kerberos = entryNumber.slice(4,7).toLowerCase() + entryNumber.slice(2,4) + entryNumber.slice(7,12);
        navigate(`/dashboard/${kerberos}`);
    }

    return (
        <section className="signin">
            <div className="login-form">
                <h2>Sign In to ClassGrid</h2>
                <form onSubmit={handleSignIn}>
                    <input id="signin-form-entryNumber" type="text" placeholder="Entry Number" onKeyUp={validateEntryNumber} required></input>
                    <button id="signin-form-submit" type="submit" disabled>Sign In</button>
                </form>
            </div>
        </section>
    )
}

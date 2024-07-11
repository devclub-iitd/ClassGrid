import React from 'react'
import './Footer.css'
import { Link } from 'react-router-dom';

export default function Footer() {

    const year = new Date().getFullYear();

    return (
        <div className="footer">
            <p>&copy; {year} Copyright : ClassGrid by DevClub, IIT Delhi</p>
            <p>Designed and Developed by : <Link to="https://www.linkedin.com/in/shashmahawar/" target='_blank'>Shashank Mahawar</Link></p>
        </div>
    )
}

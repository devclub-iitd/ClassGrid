import React from 'react'
import './Footer.css'

export default function Footer() {

    const year = new Date().getFullYear();

    return (
        <div className="footer">
            <p>&copy; {year} Copyright : ClassGrid by DevClub, IIT Delhi</p>
        </div>
    )
}

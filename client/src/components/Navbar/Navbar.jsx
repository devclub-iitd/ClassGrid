import React from 'react'
import './Navbar.css'
import { Link } from 'react-router-dom'

export default function Navbar() {
    return (
        <nav>
            <div className="navbar-logo">
                <h1>
                    <Link to="/">
                        <span className="navbar-logo-class">Class</span>
                        <span className="navbar-logo-grid">Grid</span>
                    </Link>
                </h1>
            </div>
            <div className="navbar-devclub">
                <p>
                    A <Link to="https://devclub.in" target="_blank" rel="noreferrer">DevClub</Link> Project
                </p>
            </div>
        </nav>
    )
}

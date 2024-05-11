import React from 'react'
import './Home.css'
import { Link } from 'react-router-dom'

export default function HomeComp() {
    return (
        <section>
            <div className="home">
                <div className="home-content">
                    <h2>
                        Your Semester Timetable in 2 Minutes.
                    </h2>
                    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime corporis et, magni laboriosam perferendis dicta deserunt adipisci placeat eveniet laudantium?</p>
                    <Link to="/signin">
                        <button>
                            Get Started
                        </button>
                    </Link>
                </div>
                <div className="home-hero">
                    <img src="https://via.placeholder.com/1024x1024" alt="ClassGrid" />
                </div>
            </div>
        </section>
    )
}

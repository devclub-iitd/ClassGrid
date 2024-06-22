import React from 'react'
import './Home.css'
import { Link } from 'react-router-dom'
import hero from '../../assets/hero.png'

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
                    <img src={hero} alt="ClassGrid" />
                </div>
            </div>
        </section>
    )
}

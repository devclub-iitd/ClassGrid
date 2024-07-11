import React from 'react'
import './Dashboard.css'
import EditTiming from './EditTiming';
import axios from 'axios';
import TimetableGrid from '../Timetable/TimetableGrid';

import { useMsal } from '@azure/msal-react';
import { loginRequest } from '../../authConfig';

export default function Timetable(props) {

    const name = props.name;
    const timetable = props.timetable;
    const [timetableData, setTimetableData] = React.useState({});

    const [displayGrid, setDisplayGrid] = React.useState(false);

    const { instance, accounts } = useMsal();

    React.useEffect(() => {
        for (let i = 0; i < timetable.length; i++) {
            timetableData[timetable[i].courseCode] = {
                lecture: null,
                tutorial: null,
                lab: null,
            }
            if (timetable[i].lecture) {
                timetableData[timetable[i].courseCode].lecture = [];
                for (let j = 0; j < timetable[i].lectureTiming.length; j++) {
                    if (timetable[i].lectureTiming[j].start) {
                        timetableData[timetable[i].courseCode].lecture.push({
                            day: timetable[i].lectureTiming[j].day,
                            start: timetable[i].lectureTiming[j].start,
                            end: timetable[i].lectureTiming[j].end,
                            room: timetable[i].lectureRoom,
                        });
                    }
                }
            }
        }

        setDisplayGrid(true);

    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [timetable])

    function showEditModal(courseCode) {
        document.getElementById(`edit-${courseCode}`).style.display = "block";
    }

    function generateCalendar() {
        
        instance
            .acquireTokenSilent({
                ...loginRequest,
                account: accounts[0],
            })
            .then((response) => {
                axios.post("/api/calendar/", timetableData, {
                    headers: {
                        Authorization: `Bearer ${response.accessToken}`,
                    }
                })
                .then(res => {
                    let element = document.createElement('a');
                    element.setAttribute('href', 'data:text/calendar;charset=utf-8,' + encodeURIComponent(res.data));
                    element.setAttribute('download', 'Timetable.ics');
                    element.style.display = 'none';
                    document.body.appendChild(element);
                    element.click();
                    document.body.removeChild(element);
                })
                .catch(err => {
                    console.log(err);
                })
            })
    }

    const signout = () => {
        instance.logoutRedirect({
            postLogoutRedirectUri: "/",
        });
    }

    return (
        <section className="dashboard">
            <h1>{name}'s Timetable</h1>
            <p className="logout">Not you? <span onClick={signout}>Sign out</span></p>
            <div className="timetable-container">
                {displayGrid ? <TimetableGrid timetable={timetable} timetableData={timetableData} /> : null}
                <div className="timetable-items">
                    <h2>Your courses</h2>
                    {timetable.map((course, index) => {
                        return (
                            <div className="timetable-item" key={index}>
                                <h3>{course.courseCode}</h3>
                                {course.lecture ? <p>
                                    Lectures: {course.lectureTiming.map((time, index) => {
                                        return (
                                            <>
                                                {time.start ? <span key={index}>{time.day} {time.start.slice(0,2)}:{time.start.slice(2,4)} - {time.end.slice(0,2)}:{time.end.slice(2,4)}, </span> : null}
                                            </>
                                        )
                                    })}
                                </p> : null}
                                {course.tutorial ? <p>
                                    Tutorial: <span>
                                        {timetableData[course.courseCode] ? 
                                            timetableData[course.courseCode].tutorial ? 
                                                timetableData[course.courseCode].tutorial.map((time, index) => {
                                                    return (
                                                        `${time.day} ${time.start.slice(0,2)}:${time.start.slice(2,4)} - ${time.end.slice(0,2)}:${time.end.slice(2,4)}`
                                                    )
                                                })
                                            : "Not Selected" 
                                        : "Not Selected"}
                                    </span>
                                </p> : null}
                                {course.lab ? <p>
                                    Lab: <span>
                                        {timetableData[course.courseCode] ? 
                                            timetableData[course.courseCode].lab ? 
                                                timetableData[course.courseCode].lab.map((time, index) => {
                                                    return (
                                                        `${time.day} ${time.start.slice(0,2)}:${time.start.slice(2,4)} - ${time.end.slice(0,2)}:${time.end.slice(2,4)}`
                                                    )
                                                })
                                            : "Not Selected" 
                                        : "Not Selected"}
                                    </span>
                                </p> : null}
                                {course.tutorial | course.lab | course.lectureEditable ? <><div className="timetable-edit-btn" onClick={() => showEditModal(course.courseCode)}>&#9998;</div>
                                <EditTiming div_id={`edit-${course.courseCode}`} data={course} timetableData={timetableData} setTimetableData={setTimetableData} /></> : null}
                            </div>
                        )
                    })}
                </div>
            </div>
            <button className="download-timetable-btn" onClick={generateCalendar}>
                Download Timetable
            </button>
        </section>
    )
}

import React from 'react'
import './Timetable.css'
import TimetableElement from './TimetableElement'

export default function TimetableGrid(props) {

    const timeList = ['6 AM', '7 AM', '8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM', '10 PM']

    const timetable = props.timetable;
    const data = props.timetableData;

    return (
        <div className="timetable-grid">
            <table className="time-headers">
                {timeList.map((time, index) => {
                    return (
                        <tr>
                            <td>{time}</td>
                        </tr>
                    )
                })}
            </table>
            <table className="timetable-grid-cells">
                <tr>
                    <th>Monday</th>
                    <th>Tuesday</th>
                    <th>Wednesday</th>
                    <th>Thursday</th>
                    <th>Friday</th>
                </tr>
                {timeList.map((time, index) => {

                    if (index === 0) {
                        return null
                    }

                    return (
                        <tr>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                        </tr>
                    )
                })}
                {timetable.map(course => {
                    return (
                        <>
                            {data[course.courseCode].lab ? data[course.courseCode].lab.map(lab => {
                                return <TimetableElement data={lab} course={course.courseCode} type="Lab" />;
                            }) : null}
                            {data[course.courseCode].lecture ? data[course.courseCode].lecture.map(lecture => {
                                return <TimetableElement data={lecture} course={course.courseCode} type="Lecture" />;
                            }) : null}
                            {data[course.courseCode].tutorial ? data[course.courseCode].tutorial.map(tutorial => {
                                return <TimetableElement data={tutorial} course={course.courseCode} type="Tutorial" />;
                            }) : null}
                            {/* {course.lab.map(lab => {
                                return <TimetableElement data={lab} />;
                            })}
                            {course.lecture.map(lecture => {
                                return <TimetableElement data={lecture} />;
                            })}
                            {course.lab.map(tutorial => {
                                return <TimetableElement data={tutorial} />;
                            })} */}
                        </>
                    )
                })}
            </table>
        </div>
    )
}

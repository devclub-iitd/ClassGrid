import React from 'react'
import './Timetable.css'

export default function TimetableElement(props) {

    function getStartPosition(start) {
        let hour = start.substring(0, 2);
        let minute = start.substring(2, 4);
        return (80 * ((parseInt(hour) - 6) + (parseInt(minute) / 60)) + 40);

    }

    function getDuration(start, end) {
        let startHour = start.substring(0, 2);
        let startMinute = start.substring(2, 4);
        let endHour = end.substring(0, 2);
        let endMinute = end.substring(2, 4);
        return (80 * ((parseInt(endHour) - parseInt(startHour)) + ((parseInt(endMinute) - parseInt(startMinute)) / 60)));
    }

    function getDayShift(day) {
        if (day === "Monday") {
            return 0;
        } else if (day === "Tuesday") {
            return "calc(100% / 5)";
        } else if (day === "Wednesday") {
            return "calc(100% / 5 * 2)";
        } else if (day === "Thursday") {
            return "calc(100% / 5 * 3)";
        } else if (day === "Friday") {
            return "calc(100% / 5 * 4)";
        }
    }

    return (
        <div className="timetable-element" style={{
            top: getStartPosition(props.data.start),
            height: getDuration(props.data.start, props.data.end),
            left: getDayShift(props.data.day)
        }}>
            <div className="timetable-element-left"></div>
            <h5>{props.course} - {props.type}</h5>
        </div>
    )
}

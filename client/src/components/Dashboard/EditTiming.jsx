import React from 'react'
import './Dashboard.css'

export default function EditTiming(props) {

    const data = props.data;
    const timetableData = props.timetableData;
    const setTimetableData = props.setTimetableData;

    function saveData() {
        let courseCode = data.courseCode;
        let temp = timetableData[courseCode];
        let master_div = document.getElementById(props.div_id);

        if (data.tutorial) {
            let tutorial = master_div.querySelector("#select-tutorial").value;
            if (tutorial !== "0") {
                temp.tutorial = [{
                    day: tutorial.split(" ")[0],
                    start: tutorial.split(" ")[1],
                    end: tutorial.split(" ")[2]
                }]
                if (temp.tutorial.start >= temp.tutorial.end) {
                    temp.tutorial = null;
                }
            } else {
                temp.tutorial = null;
            }
        }

        if (data.lab) {
            let labDay = master_div.querySelector("#select-lab-day").value;
            let labStart = master_div.querySelector("#lab-start").value;
            let labEnd = master_div.querySelector("#lab-end").value;
            if (labDay !== "0") {
                temp.lab = [{
                    day: labDay,
                    start: labStart.replace(":", ""),
                    end: labEnd.replace(":", "")
                }]
                if (temp.lab.start >= temp.lab.end) {
                    temp.lab = null;
                }
            } else {
                temp.lab = null;
            }
        }
        
        setTimetableData(prevState => ({
            ...prevState,
            [courseCode]: temp
        }));
        console.log(timetableData);
        document.getElementById(props.div_id).style.display = "none";
    }

    return (
        <div className="edit-timing-modal" id={props.div_id}>
            <div className="edit-timing-inner">
                <h4>Editing {data.courseCode}</h4>
                {data.tutorial && data.tutorialTiming ? <div className="edit-timing-section">
                    <h5>Tutorial</h5>
                    <select name="tutorial" id="select-tutorial">
                        <option value="0" selected disabled>Not Selected</option>
                        {data.tutorialTiming.map((time, index) => {
                            return (
                                time.start ? <option key={index} value={`${time.day} ${time.start} ${time.end}`}>{time.day} {time.start.slice(0,2)}:{time.start.slice(2,4)} - {time.end.slice(0,2)}:{time.end.slice(2,4)}</option> : null
                            )
                        })}
                    </select>
                </div> : null}
                {data.lab ? <div className="edit-timing-section">
                    <h5>Lab</h5>
                    <select name="lab" id="select-lab-day">
                        <option value="0" selected disabled>Select Day</option>
                        <option value="Monday">Monday</option>
                        <option value="Tuesday">Tuesday</option>
                        <option value="Wednesday">Wednesday</option>
                        <option value="Thursday">Thursday</option>
                        <option value="Friday">Friday</option>
                    </select>
                    <div className="select-lab-time">
                        <div className="select-lab-time-comp">
                            <p>Start Time</p>
                            <input type="time" name="lab-start" id="lab-start" />
                        </div>
                        <div className="select-lab-time-comp">
                            <p>End Time</p>
                            <input type="time" name="lab-end" id="lab-end" />
                        </div>
                    </div>
                </div> : null}
                <button onClick={saveData}>Save</button>
            </div>
        </div>
    )
}

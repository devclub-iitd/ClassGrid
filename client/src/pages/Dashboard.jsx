import React from 'react'
import FetchingCourses from '../components/Dashboard/FetchingCourses';
import Courses from '../components/Dashboard/Courses';
import { useParams } from 'react-router-dom';
import Timetable from '../components/Dashboard/Timetable';
import SettingUp from '../components/Dashboard/SettingUp';

export default function Dashboard(props) {

    const kerberos = useParams().kerberos;
    const setTitle = props.setTitle;
    const setProgress = props.setProgress;

    React.useEffect(() => {
        setTitle("My Dashboard | ClassGrid | DevClub - IIT Delhi")
        setProgress(25);

    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    const [navigation, setNavigation] = React.useState(0);
    const [name, setName] = React.useState();
    const [courses, setCourses] = React.useState([]);
    const [timetable, setTimetable] = React.useState({});

    return (
        <>
            {navigation === 0 ? <FetchingCourses kerberos={kerberos} setName={setName} setCourses={setCourses} setNavigation={setNavigation} setProgress={setProgress} /> : null}
            {navigation === 1 ? <Courses name={name} courses={courses} setNavigation={setNavigation} /> : null}
            {navigation === 2 ? <SettingUp kerberos={kerberos} setName={setName} setTimetable={setTimetable} setNavigation={setNavigation} setProgress={setProgress} /> : null}
            {navigation === 3 ? <Timetable name={name} timetable={timetable} setNavigation={setNavigation} /> : null}
        </>
    )
}

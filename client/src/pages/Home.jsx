import React from 'react'
import HomeComp from '../components/Home/Home'

export default function Home(props) {

    const setTitle = props.setTitle;
    const setProgress = props.setProgress;

    React.useEffect(() => {
        setTitle("ClassGrid by DevClub - Your Semester Timetable in 2 Minutes")
        setProgress(100);

    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    return (
        <HomeComp />
    )
}

import React, { useState, useEffect } from "react";
import EntryMain from './entryMain.jsx';
import NonEntryMain from './nonEntryMain.jsx';
import "./Main.css";
import { defaultInstance as api } from '../../util/token';

const TurtlebotController = ( ) =>{
    const [isEntry, setIsEntry] = useState(false);

    const userId = localStorage.getItem('userId');

    useEffect(() => {
        const url = "/robot/exist?id=" + userId
        api.get(url)
        .then(response => {
            setIsEntry(true);
            localStorage.setItem('turtlebot', response.data.serial_number);
        })
        .catch(error => {
            console.error('에러 발생:', error);
            setIsEntry(false);
        });
        
    }, []);
    
    return (
    <div className="controllerContainer" >
        {
            isEntry?
            <EntryMain />
            :
            <NonEntryMain />
        }
    </div>
    );
};

export default TurtlebotController;
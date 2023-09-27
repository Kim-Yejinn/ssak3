import React, { useState, useEffect } from "react";
import EntryMain from './entryMain.jsx';
import NonEntryMain from './nonEntryMain.jsx';
import "./Main.css";
import { defaultInstance as api } from '../../util/token';

const TurtlebotController = ( ) =>{
    const [isEntry, setIsEntry] = useState(true);

    // const isEntry = localStorage.getItem('turtlebot');

    const formdata = {
        "id" : "qwe"
    }

    // useEffect(() => {
    //     // axios 요청을 보내고 데이터를 받아옴
    //     try {
    //         console.log(1)
    //         const response = api.get("/robot/exist",formdata);
    //         console.log(response.data)
    //         console.log(3)
    //     } catch (error) {
    //         console.error(error);
    //     }

    // }, []);
    
    // 나중에 이거 GET으로 받아오는 기능으로 변경
    return (
    // Figma : main - 터틀봇 등록돼있는 상태
    // ㄴ controllerContainer : UI
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
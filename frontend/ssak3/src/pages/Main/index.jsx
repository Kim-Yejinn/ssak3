import React from "react";
import EntryMain from './entryMain.jsx';
import NonEntryMain from './nonEntryMain.jsx';
import "./Main.css";

const TurtlebotController = ( ) =>{
    let isEntry = true;
    // 나중에 이거 GET으로 받아오는 기능으로 변경
    return (
    // Figma : main - 터틀봇 등록돼있는 상태
    // ㄴ controllerContainer : UI
    <div className="controllerContainer" >
        {
            isEntry ?
            <EntryMain />
            :
            <NonEntryMain />
        }
    </div>
    );
};

export default TurtlebotController;
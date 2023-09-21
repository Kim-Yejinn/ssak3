import React from "react";
import styles from "./style.css";

const turtleBotStarter = () =>{
    return ( 
    <div className="controlContainer">
        <div>
            <div className="title">터틀봇 제어</div>
        </div>
        <div>
            <div className="menuOn">세탁물 설정</div>
            <div className="menuOff">스케줄</div>
        </div>
    </div> 
    );
};

export default turtleBotStarter;
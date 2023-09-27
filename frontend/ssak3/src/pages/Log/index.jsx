import React, {useState} from "react";
import Log from "./log.jsx";
import styles from "./style.css";

const TurtleBotLog = () =>{
    // 초기 상태
    const [isSetting, setIsSetting] = useState(true);
    const toggleIsSetting = () => {
        setIsSetting(!isSetting);
    };
    return ( 
        <div className="container">
            <div className="nav">
                <div className="title">터틀봇 활동기록</div>
            </div>
            <Log />
                
        </div> 
    );
};

export default TurtleBotLog;
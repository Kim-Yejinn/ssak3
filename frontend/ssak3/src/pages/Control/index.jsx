import React, {useState} from "react";
import Controller from "./controller.jsx";
import Scheduler from "./scheduler.jsx";
import styles from "./style.css";

const TurtleBotStarter = () =>{
    // 초기 상태
    const [isSetting, setIsSetting] = useState(true);
    const toggleIsSetting = () => {
        setIsSetting(!isSetting);
    };
    return ( 
    <div className="container">
        <div className="nav">
            <div className="starterTitle">터틀봇 제어</div>
            <div className="back"></div>
        </div>
        <div className="starterContents">
            <div>
                <div className="set"><div className="starterContentOn">세탁물 설정</div></div>
                <div className="schedule"></div>
                <Controller />
            </div>
        </div>
    </div> 
    );
};

export default TurtleBotStarter;
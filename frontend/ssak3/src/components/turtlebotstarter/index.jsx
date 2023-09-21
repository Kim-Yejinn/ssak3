import React, {useState} from "react";
import SetClothes from "./SetClothes.jsx";
import Scheduler from "./scheduler";
import styles from "./style.css";

const TurtleBotStarter = () =>{
    // 초기 상태
    const [isSetting, setIsSetting] = useState(true);
    const toggleIsSetting = () => {
        setIsSetting(!isSetting);
    };
    return ( 
    <div className="controlContainer">
        <div className="nav">
            { isSetting ? 
            <div className="title">터틀봇 제어</div>
            :
            <div className="title">터틀봇 활동기록</div>
            }
        </div>
        <div className="menu">
            { isSetting ? 
            <div>
                <div className="set"><div className="menuOn">세탁물 설정</div></div>
                <div className="schedule" onClick={toggleIsSetting}><div className="menuOff">스케줄</div></div>
                <SetClothes />
            </div>
            :
            <div>
                <div className="set" onClick={toggleIsSetting}><div className="menuOff">세탁물 설정</div></div>
                <div className="schedule"><div className="menuOn">스케줄</div></div>
                <Scheduler />
            </div>
            }
        </div>
            
    </div> 
    );
};

export default TurtleBotStarter;
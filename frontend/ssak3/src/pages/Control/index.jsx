import React, {useState} from "react";
import Controller from "./controller.jsx";
import { useNavigate } from "react-router-dom";
import "./style.css";

const TurtleBotStarter = () =>{
    // 초기 상태
    const navigate = useNavigate();

    const GoMain = () => {
        navigate("/main");
    };
    const [isSetting, setIsSetting] = useState(true);
    const toggleIsSetting = () => {
        setIsSetting(!isSetting);
    };
    return ( 
    <div className="container">
        <div className = "areah-10 justalign-center">
                <div onClick={GoMain} className = "addtbackbutton">‹</div>
                <div className = "areaw-80 justalign-center">터틀봇 제어</div>
                <div className = "areaw-20 justalign-center"></div>
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
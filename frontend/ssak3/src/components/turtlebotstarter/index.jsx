import React, {useState} from "react";
import styles from "./style.css";

const TurtleBotStarter = () =>{
    // 초기 상태
    const [starIsVisible, setStarIsVisible] = useState(false);
    const [isVisible, setIsVisible] = useState(false);
    const starToggleVisibility = () =>{
        setStarIsVisible(!starIsVisible);
    };
    const toggleVisibility = () => {
        setIsVisible(!isVisible);
    };
    return ( 
    <div className="controlContainer">
        <div className="nav">
            <div className="title">터틀봇 제어</div>
        </div>
        <div className="menu">
            <div className="menuOn">세탁물 설정</div>
            <div className="menuOff">스케줄</div>
        </div>
        <div className="container">
            <div className="starFrame">
                <div className="starLogoFrame"></div>
                <div className="starBtn"></div>
                <div className="starTitle">T-shirt</div>
                { starIsVisible ?
                <div>
                    <div className="starOnText">On</div>
                    <div className="starToggleOnBg">
                        <div className="starToggleOn" onClick={starToggleVisibility}></div>
                    </div>
                </div>
                :
                <div>
                    <div className="offText">Off</div>
                    <div className="starToggleOffBg">
                        <div className="starToggleOff" onClick={starToggleVisibility}></div>
                    </div>
                </div>
                }
            </div>
            <div className="unstarFrame">
                <div className="logoFrame"></div>
                <div className="unStarBtn"></div>
                <div className="unstarTitle">Pants</div>
                {isVisible ?
                <div>
                    <div className="unstarOnText">On</div>
                    <div className="toggleOnBg">
                        <div className="toggleOn" onClick={toggleVisibility}></div>
                    </div>
                </div>
                :
                <div>
                    <div className="offText">Off</div>
                    <div className="toggleOffBg">
                        <div className="toggleOff" onClick={toggleVisibility}></div>
                    </div>
                </div>
                }

            </div>      
        </div>
        <div className="startBtn">
            주행하기
        </div>
    </div> 
    );
};

export default TurtleBotStarter;
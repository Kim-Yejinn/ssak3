import React from "react";
import styles from "./style.css";

const NonEntryMain = ( ) =>{
    return (
        <div>
            {/* // Figma : main/More - "터틀봇 - 시리얼 넘버"
            // ㄴ turtlebotName : 터틀봇 시리얼넘버와 이름 */}
            <div className="turtlebotName" >TurtleBot - 미등록</div>
            <div className="turtlebotUnconnectedImage" ></div>
            <div className="unconnectedMessage"> 연결된 기기가 없습니다. </div>
            <div className="menu-border">
                <div className="menu">
                    <div className="frame" >
                        <div className="frameBlank"></div>
                        <div className="subFrame" >
                            <div className="subFrameBlank" ></div>
                            <div className="menuTitle" >기기 등록하기</div>
                        </div>
                        <div className="frameBlank" ></div>    
                        <div className="rightArrowFrame" >
                                <div className="rightArrow" ></div>
                        </div>
                    </div>
                </div>
                <div className="menu" >
                    <div className="frame" >
                        <div className="frameBlank"></div>
                        <div className="subFrame">
                            <div className="subFrameBlank"></div>
                            <div className="menuTitle" >홈으로 돌아가기</div>
                        </div>
                        <div className="frameBlank" ></div>    
                        <div className="rightArrowFrame" >
                                <div className="rightArrow" ></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default NonEntryMain;
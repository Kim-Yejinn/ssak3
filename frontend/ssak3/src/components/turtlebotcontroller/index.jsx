import React from "react";
import styles from "./style.css";

const TurtlebotController = ( ) =>{
    let name = "TurtleBot - TB230911_1"; 
    // 나중에 이거 GET으로 받아오는 기능으로 변경
    return (
    // Figma : main - 터틀봇 등록돼있는 상태
    // ㄴ controllerContainer : UI
    <div className="controllerContainer" >
        {/* // Figma : main/More - "터틀봇 - 시리얼 넘버"
            // ㄴ turtlebotName : 터틀봇 시리얼넘버와 이름 */}
        <div className="turtlebotName" >{ name }</div>
        <div className="turtlebotImage" ></div>
        <div className="menu-border">
            <div className="menu">
                <div className="frame" >
                    <div className="frameBlank"></div>
                    <div className="subFrame" >
                        <div className="subFrameBlank" ></div>
                        <div className="title" >터틀봇 제어</div>
                        <div className="subTitle" >작동중</div>
                    </div>
                    <div className="frameBlank" ></div>    
                    <div className="rightArrowFrame" >
                            <div className="rightArrow" >></div>
                    </div>
                </div>
            </div>
            <div className="menu" >
                <div className="frame" >
                    <div className="frameBlank" ></div>
                    <div className="subFrame" >
                        <div className="subFrameBlank" ></div>
                        <div className="title" >날씨 정보</div>
                        <div className="subTitle" >실내온도 20℃</div>
                    </div>
                    <div className="frameBlank" ></div>    
                    <div className="rightArrowFrame" >
                            <div className="rightArrow" >></div>
                    </div>
                </div>
            </div>
            <div className="menu">
                <div className="frame" >
                    <div className="frameBlank" ></div>
                    <div className="subFrame" >
                        <div className="subFrameBlank" ></div>
                        <div className="title">사용 기록</div>
                        <div className="subTitle">최근 사용</div>
                    </div>
                    <div className="frameBlank"></div>    
                    <div className="rightArrowFrame" >
                            <div className="rightArrow">></div>
                    </div>
                </div>
            </div>
            <div className="menu">
                <div className="frame" >
                    <div className="frameBlank"></div>
                    <div className="subFrame" >
                        <div className="subFrameBlank" ></div>
                        <div className="title" >시간 설정</div>
                        <div className="subTitle">예약 설정</div>
                    </div>
                    <div className="frameBlank"></div>    
                    <div className="rightArrowFrame" >
                            <div className="rightArrow">></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    );
};

export default TurtlebotController;
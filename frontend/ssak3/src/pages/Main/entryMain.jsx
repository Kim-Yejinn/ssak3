import React from "react";
import "./Main.css";

const EntryMain = ( ) =>{
    let name = "TurtleBot - TB230911_1";
    // 나중에 이거 GET으로 받아오는 기능으로 변경
    return (
    // Figma : main - 터틀봇 등록돼있는 상태
    // ㄴ controllerContainer : UI
    <div>
        <div className="turtlebotName" >{ name }</div>
        <div className="turtlebotImage" ></div>
        <div className="menu-border">
            <div className="menu">
                <div className="frame" >
                    <div className="frameBlank"></div>
                    <div className="subFrame" >
                        <div className="subFrameBlank" ></div>
                        <div className="menuTitle" >터틀봇 제어</div>
                        <div className="menuSubtitle" >작동중</div>
                    </div>
                    <div className="frameBlank" ></div>    
                    <div className="rightArrowFrame" >
                            <div className="rightArrow" ></div>
                    </div>
                </div>
            </div>
            <div className="menu" >
                <div className="frame" >
                    <div className="frameBlank" ></div>
                    <div className="subFrame" >
                        <div className="subFrameBlank" ></div>
                        <div className="menuTitle" >날씨 정보</div>
                        <div className="menuSubtitle" >실내온도 20℃</div>
                    </div>
                    <div className="frameBlank" ></div>    
                    <div className="rightArrowFrame" >
                            <div className="rightArrow" ></div>
                    </div>
                </div>
            </div>
            <div className="menu">
                <div className="frame" >
                    <div className="frameBlank" ></div>
                    <div className="subFrame" >
                        <div className="subFrameBlank" ></div>
                        <div className="menuTitle">사용 기록</div>
                        <div className="menuSubtitle">최근 사용</div>
                    </div>
                    <div className="frameBlank"></div>    
                    <div className="rightArrowFrame" >
                            <div className="rightArrow"></div>
                    </div>
                </div>
            </div>
            <div className="menu">
                <div className="frame" >
                    <div className="frameBlank"></div>
                    <div className="subFrame" >
                        <div className="subFrameBlank" ></div>
                        <div className="menuTitle" >시간 설정</div>
                        <div className="menuSubtitle">예약 설정</div>
                    </div>
                    <div className="frameBlank"></div>    
                    <div className="rightArrowFrame" >
                            <div className="rightArrow"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    );
};

export default EntryMain;
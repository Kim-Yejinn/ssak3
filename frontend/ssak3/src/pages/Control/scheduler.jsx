import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import "./ScheduleStyle.css";

const Scheduler = () => {
    const navigate = useNavigate();

    const GoMain = () => {
        navigate("/main");
    };

    const GoAdd = () => {
        navigate("/addschedule");
    };

    const [scheduleToggle, setScheduleToggle] = useState(true);

    const scheduleToggleClick = () => {
        setScheduleToggle(!scheduleToggle);
    };

    const [isModal, setIsModal] = useState(false);

    const modalClick = () => {
        setIsModal(!isModal);
    };

    let score = "T-shirt: 1 Pants: 2"

    return (
    <div className="main-container">
        <div className = "areah-20">
            <div className = "areah-40 justalign-center">
                <div onClick={GoMain} className = "addtbackbutton">‹</div>
                <div className = "areaw-80 justalign-center">스케줄</div>
                <div className = "areaw-20 justalign-center"></div>
            </div>
            <div className = "addttitle">
                <div>스케줄 목록</div>
            </div>
        </div>
        <div className = "areah-80">
            <div className="areah-75 justalign-center">
                <div className = "schdulebox">
                    <div className = "areah-10 justalign-center">
                        <div className = "areaw-20 justalign-center fontchange">스케줄 (1)</div>
                        <div className = "areaw-60"></div>
                        <div className = "areaw-20 justalign-center fontchange">Ⅴ 시간순</div>
                    </div>
                    <div className="scheduleBox">
                        <div className="scheduleBoxTitle">평일 퇴근 시간</div>
                        {
                            scheduleToggle ?
                            <div className="scheduleToggleOnBg" onClick={scheduleToggleClick}>
                                <div className="scheduleToggleOn" onClick={scheduleToggleClick}></div>
                            </div>
                            :
                            <div className="scheduleToggleOffBg" onClick={scheduleToggleClick}>
                                <div className="scheduleToggleOff" onClick={scheduleToggleClick}></div>
                            </div>
                        }
                        <div className="scheduleBoxLine"></div>
                        <div className="scheduleBoxTimeImage"></div>
                        <div className="scheduleBoxTime"> 06 : 00</div>
                        <div className="scheduleBoxDayImage"></div>
                        <div className="scheduleBoxDay"> Mon, Wed, Fri, Sat</div>
                        <div className="scheduleBoxDetail" onClick={modalClick}></div>
                        {isModal && (
                            <div className="modal-overlay">
                            <div className="modal">
                                <h2>세탁물 수거 정보</h2>
                                <div className="detailInfo">
                                    <div className="detailInfoDate">YYYY-MM-DD</div>
                                    <div className="detailInfoTime">HH:MM:SS~HH:MM:SS</div>
                                    <p className="detailInfoScore"> {score}</p>
                                </div>
                                <button onClick={modalClick}>닫기</button>
                            </div>
                            </div>
                        )}
                    </div>
                </div>

                {/* <div className="scheduleCount" style={{border:'1px solid red'}}>스케줄 (0)</div>
                <div className="timeSort">Ⅴ 시간순</div>
                <div className="scheduleBox">
                    <div className="scheduleBoxTitle">평일 퇴근 시간</div>
                    {
                        scheduleToggle ?
                        <div className="scheduleToggleOnBg" onClick={scheduleToggleClick}>
                            <div className="scheduleToggleOn" onClick={scheduleToggleClick}></div>
                        </div>
                        :
                        <div className="scheduleToggleOffBg" onClick={scheduleToggleClick}>
                            <div className="scheduleToggleOff" onClick={scheduleToggleClick}></div>
                        </div>
                    }
                    <div className="scheduleBoxLine"></div>
                    <div className="scheduleBoxTimeImage"></div>
                    <div className="scheduleBoxTime"> 06 : 00</div>
                    <div className="scheduleBoxDayImage"></div>
                    <div className="scheduleBoxDay"> Mon, Wed, Fri, Sat</div>
                    <div className="scheduleBoxDetail" onClick={modalClick}></div>
                    {isModal && (
                        <div className="modal-overlay">
                        <div className="modal">
                            <h2>세탁물 수거 정보</h2>
                            <div className="detailInfo">
                                <div className="detailInfoDate">YYYY-MM-DD</div>
                                <div className="detailInfoTime">HH:MM:SS~HH:MM:SS</div>
                                <p className="detailInfoScore"> {score}</p>
                            </div>
                            <button onClick={modalClick}>닫기</button>
                        </div>
                        </div>
                    )}
                </div> */}
            </div>
            <div onClick={GoAdd} className = "areah-25 justalign-center">
                <div className="addschedulebutton">스케줄 추가</div>
            </div>
        </div>
    </div> 
    );

}

export default Scheduler;
import React, { useState } from 'react';
import axios from 'axios';

const Scheduler = () => {
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
        <div>
            <div className="scheduleContainer">
                <div className="scheduleCount">스케줄 (0)</div>
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
                </div>
                <button className="addBtn">
                    스케줄 추가
            </button>
            </div>
        </div>
    );

}

export default Scheduler;
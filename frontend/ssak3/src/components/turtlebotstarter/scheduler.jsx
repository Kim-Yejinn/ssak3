import React, { useState } from 'react';
import styles from "./style.css";
import axios from 'axios';

const Scheduler = () => {
    return (
        <div>
            <div className="scheduleContainer">
                <div className="scheduleCount">스케줄 (0)</div>
                <div className="timeSort">Ⅴ 시간순</div>
                <div className="scheduleBox">
                    <div className="proceedingTitle">YYYY-MM-DD_TASK0</div>
                    <div className="proceedingPredict">예상 시간 : 00분</div>
                    <div className="loadingGif"></div>
                </div>
                <div className="scheduleBox">
                    <div className="proceedingTitle">YYYY-MM-DD_TASK0</div>
                    <div className="proceedingPredict">예상 시간 : 00분</div>
                    <div className="loadingGif"></div>
                </div>
                <button className="addBtn">
                    스케줄 추가
            </button>
            </div>
            
        </div>
    );

}

export default Scheduler;
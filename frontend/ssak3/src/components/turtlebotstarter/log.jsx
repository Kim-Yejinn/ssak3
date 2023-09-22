import React from "react";
import styles from "./style.css";

const scheduler = () => {
    return (
        <div className="scheduleBox">
            <div className="logCount">빨래 기록 (4)</div>
            <div className="timeSort">Ⅴ 시간순</div>
            {/* <div className="timeSort">
                <select value={selectedTime} onChange={handleSelectChange}>
                    <option value="">시간을 선택하세요</option>
                    {times.map((time, index) => (
                    <option key={index} value={time}>
                        {time}
                    </option>
                    ))}
                </select>
            </div> */}
            <div className="logBox">
                <div className="proceedingTitle">YYYY-MM-DD_TASK0</div>
                <div className="proceedingPredict">예상 시간 : 00분</div>
                <div className="loadingGif"></div>
                <div className="proceedingStartTime">시작 시간 HH:MM</div>
                <div className="proceedingScore">현재까지 수거량 : 00</div>
            </div>
            <div className="logBox">
                <div className="logTitle">YYYY-MM-DD_TASK0</div>
                <div className="logScore">총 수거량 : 00</div>
                <div className="logTime">HH:MM ~ HH:MM</div>
                
            </div>
        </div>
    );
}
export default scheduler;
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
            <div className="cleaningBox">

            </div>
            <div className="cleaningBox">

            </div>
        </div>
    );
}
export default scheduler;
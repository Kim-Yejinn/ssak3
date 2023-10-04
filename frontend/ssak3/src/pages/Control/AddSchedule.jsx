import React, { useState } from "react";
import "./ScheduleStyle.css";
import { useNavigate } from "react-router-dom";
import { defaultInstance as api } from '../../util/token.jsx';

const AddSchedule = () => {
    const navigate = useNavigate();

    const GoMain = () => {
        navigate("/main");
    };

    const [hourValue, setHourValue] = useState(12);
    const [inputTitle, setInputTitle] = useState('');

    const formatHour = (value) => {
        return value.toLocaleString(undefined, { minimumIntegerDigits: 2 });
    };

    const handleInputChange = (event) => {
        setInputTitle(event.target.value);
    };

    const addhour = (e) => {
        e.preventDefault()
        if (hourValue == 22){
            setHourValue(0);
        }else{
            setHourValue(hourValue + 2);
        }
    };
    const decreasehour = (e) => {
        e.preventDefault()
        if (hourValue == 0){
            setHourValue(22);
        }else{
            setHourValue(hourValue - 2);
        }
    };

    const formdata = {
        "memberId" : 1,
	    "laundry" : ["shirts", "pants"],
	    "time" : hourValue
    }

    const sendaddschedule = async (event) => {
        event.preventDefault();
        try {
            const response = await api.post("/robot/run", formdata);
            console.log('등록성공', response);
            navigate('/main');
        } catch (error) {
            console.error(error);
            alert("오류가 발생했습니다.");
        }
    };

    return(
    <div className="main-container">
        <div className = "areah-20">
            <div className = "areah-40 justalign-center">
                <div onClick={GoMain} className = "addtbackbutton">‹</div>
                <div className = "areaw-80 justalign-center">터틀봇 제어</div>
                <div className = "areaw-20 justalign-center"></div>
            </div>
            <div className = "addttitle">
                <div>스케줄 추가</div>
            </div>
        </div>
        <div className = "areah-80">
            <div className = "areah-75">
                <div className = "areah-25 justalign-center">
                    <div>
                        <label for="title">제목</label><br/>
                        <input type="text" id="title" value={inputTitle} onChange={handleInputChange} placeholder="title" required/>
                    </div>
                </div>
                <div className = "areah-55 justalign-center">
                    <div>
                        <div className="timetitle">시간</div><br/>
                        <div className="timebox">
                            <div className = "areaw-30">
                                <div className="addttimea" onClick={decreasehour}>{hourValue == 0 ? 22 : formatHour(hourValue - 2)}</div>
                                <div className="addttimeb">{formatHour(hourValue)}</div>
                                <div className="addttimea" onClick={addhour}>{hourValue === 24 ? formatHour(0) : formatHour(hourValue + 2)}</div>
                            </div>
                            <div className = "areaw-10">
                                <div className="addttimea"></div>
                                <div className="addttimeb">:</div>
                                <div className="addttimea"></div>
                            </div>
                            <div className = "areaw-30">
                                <div className="addttimea">59</div>
                                <div className="addttimeb">{formatHour(0)}</div>
                                <div className="addttimea">{formatHour(1)}</div>
                            </div>
                            <div className = "areaw-30">
                                <div className="addttimea">AM</div>
                                <div className="addttimeb">PM</div>
                                <div className="addttimea"></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className = "areah-20 justalign-center">
                    <div>
                        <div className="daytitle">요일</div><br/>
                        <div className="daybox">
                            <div className = "addtdaya">Mon</div>
                            <div className = "addtdayb">Tue</div>
                            <div className = "addtdayb">Wed</div>
                            <div className = "addtdaya">Thu</div>
                            <div className = "addtdayb">Fri</div>
                            <div className = "addtdayb">Sat</div>
                            <div className = "addtdaya">Sun</div>
                        </div>
                    </div>
                </div>
            </div>
            <div className = "areah-25 justalign-center">
                <div className="addschedulebutton">스케줄 추가</div>
            </div>
        </div>
    </div>
    );
};

export default AddSchedule;
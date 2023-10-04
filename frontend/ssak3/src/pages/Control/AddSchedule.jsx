import React, { useState } from "react";
import "./ScheduleStyle.css";
import { useNavigate } from "react-router-dom";
import axios from 'axios';

const AddSchedule = () => {
    const navigate = useNavigate();

    const GoSchedule = () => {
        navigate("/schedule");
    };

    const [hourValue, setHourValue] = useState(6);
    const [minValue, setMinValue] = useState(30);
    const [meridiemValue, setMeridiemValue] = useState("AM");


    const [inputTitle, setInputTitle] = useState('');

    const formatHour = (value) => {
        return value.toLocaleString(undefined, { minimumIntegerDigits: 2 });
    };

    const handleInputChange = (event) => {
        setInputTitle(event.target.value);
    };

    const addhour = (e) => {
        e.preventDefault()
        if (hourValue == 12){
            setHourValue(1);
        }else{
            setHourValue(hourValue + 1);
        }
    };
    const decreasehour = (e) => {
        e.preventDefault()
        if (hourValue == 1){
            setHourValue(12);
        }else{
            setHourValue(hourValue - 1);
        }
    };

    const addmin = (e) => {
        e.preventDefault()
        if (minValue == 59){
            setMinValue(0);
        }else{
            setMinValue(minValue + 1);
        }
    };
    const decreasemin = (e) => {
        e.preventDefault()
        if (minValue == 0){
            setMinValue(59);
        }else{
            setMinValue(minValue - 1);
        }
    };

    const changemeridium = (e) => {
        e.preventDefault()
        if (meridiemValue === "AM"){
            setMeridiemValue("PM");
        }else{
            setMeridiemValue("AM");
        }
    };

    const formdata = {
        "auth_id": localStorage.getItem("userId"),
        "title": inputTitle,
        "meridiem": meridiemValue,
        "hour": hourValue,
        "minute": minValue,
        "date": [0,1,2,3,4,5,6]
    }

    const sendaddschedule = async (event) => {
        event.preventDefault();
        axios.post('http://j9b201.p.ssafy.io:8081/schedule', formdata)
        .then(response => {
            console.log('등록성공', response);
            GoSchedule();
        })
        .catch(error => {
            console.error(error);
            alert("오류가 발생했습니다.");
        });
    };

    return(
    <div className="main-container">
        <div className = "areah-20">
            <div className = "areah-40 justalign-center">
                <div onClick={GoSchedule} className = "addtbackbutton">‹</div>
                <div className = "areaw-80 justalign-center">스케줄</div>
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
                                <div className="addttimea" onClick={decreasehour}>{hourValue == 1 ? 12 : formatHour(hourValue - 1)}</div>
                                <div className="addttimeb">{formatHour(hourValue)}</div>
                                <div className="addttimea" onClick={addhour}>{hourValue === 12 ? formatHour(1) : formatHour(hourValue + 1)}</div>
                            </div>
                            <div className = "areaw-10">
                                <div className="addttimea"></div>
                                <div className="addttimeb">:</div>
                                <div className="addttimea"></div>
                            </div>
                            <div className = "areaw-30">
                                <div className="addttimea" onClick={decreasemin}>{minValue == 0 ? 59 : formatHour(minValue - 1)}</div>
                                <div className="addttimeb">{formatHour(minValue)}</div>
                                <div className="addttimea" onClick={addmin}>{minValue === 59 ? formatHour(0) : formatHour(minValue + 1)}</div>
                            </div>
                            <div className = "areaw-30">
                                <div onClick={changemeridium} className="addttimea">{meridiemValue === "PM" ? "AM" : " " }</div>
                                <div className="addttimeb">{meridiemValue}</div>
                                <div onClick={changemeridium} className="addttimea">{meridiemValue === "AM" ? "PM" : " " }</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className = "areah-20 justalign-center">
                    <div>
                        <div className="daytitle">요일</div><br/>
                        <div className="daybox">
                            <div className = "addtdaya">Mon</div>
                            <div className = "addtdaya">Tue</div>
                            <div className = "addtdaya">Wed</div>
                            <div className = "addtdaya">Thu</div>
                            <div className = "addtdaya">Fri</div>
                            <div className = "addtdaya">Sat</div>
                            <div className = "addtdaya">Sun</div>
                        </div>
                    </div>
                </div>
            </div>
            <div className = "areah-25 justalign-center">
                <div onClick={sendaddschedule} className="addschedulebutton">등록</div>
            </div>
        </div>
    </div>
    );
};

export default AddSchedule;
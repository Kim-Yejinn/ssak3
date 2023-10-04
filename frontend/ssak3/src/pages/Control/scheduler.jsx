import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import "./ScheduleStyle.css";
import { defaultInstance as api } from '../../util/token';

const Scheduler = () => {
    const url = "https://j9b201.p.ssafy.io/api/schedule";

    const navigate = useNavigate();

    const GoMain = () => {
        navigate("/main");
    };

    const GoAdd = () => {
        navigate("/addschedule");
    };

    const GoDetail = (event, value) => {
        event.preventDefault();
        navigate("/detailschedule", { state: { schedule_id: value } });
    };

    const [schedule, setSchedule] = useState([]);

    useEffect(()=>{
        getSchedule();
    },[]);

    const getSchedule = async () => {
        axios.get(url+"?auth_id="+localStorage.getItem("userId"))
        .then(response => {
            console.log(response);
            setSchedule(response.data);
            console.log(response.data);
        })
        .catch(error => {
            window.alert("로그를 불러오는 중 문제가 발생했습니다.");
            console.error(error);
        });
    };

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
                        <div className = "areaw-20 justalign-center fontchange">스케줄 ({schedule.length})</div>
                        <div className = "areaw-60"></div>
                        <div className = "areaw-20 justalign-center fontchange">등록순</div>
                    </div>
                    {schedule.map((item, index) => (
                        <div className="scheduleBox">
                            <div className="scheduleBoxTitle">{item.title}</div>
                            <div className="scheduleBoxLine"></div>
                            <div className="scheduleBoxTimeImage"></div>
                            <div className="scheduleBoxTime">{item.time}</div>
                            <div className="scheduleBoxDayImage"></div>
                            <div className="scheduleBoxDay">{item.day}</div>
                            <div className="scheduleBoxDetail" onClick={(event) => GoDetail(event, item.id)}></div>
                        </div>
                    ))}
                </div>
            </div>
            <div onClick={GoAdd} className = "areah-25 justalign-center">
                <div className="addschedulebutton">스케줄 추가</div>
            </div>
        </div>
    </div> 
    );

}

export default Scheduler;
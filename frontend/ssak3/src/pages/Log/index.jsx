import React,{ useEffect, useState } from "react";
import "./style.css";
import { defaultInstance as api } from '../../util/token';
import { useNavigate } from "react-router-dom";

const TurtleBotLog = () =>{
    const navigate = useNavigate();

    const GoMain = () => {
        navigate("/main");
    };

    const [log, setLog] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(()=>{
        getLog();
    },[]);
    const getLog = () => {
        api.get("/robot/log?id="+localStorage.getItem("userId"))
        .then((res)=>{
            console.log(res);
            setLog(res.data);
            setLoading(false);
        }).catch((err)=>{
            window.alert("로그를 불러오는 중 문제가 발생했습니다.");
        })
    };
    const formatLog = (value) => {
        return value.replace("T", " ");
    };
    return ( 
        <div className="container">
            <div className = "areah-10 justalign-center">
                <div onClick={GoMain} className = "addtbackbutton">‹</div>
                <div className = "areaw-80 justalign-center">사용 기록</div>
                <div className = "areaw-20 justalign-center"></div>
            </div>
            {
                    loading ?
                    <div className="logContainer">
                        <div className="axiosLoadingGif"/>
                    </div>
                    :    
                    <div className="logContainer">
                        <div className="logCount">빨래 기록 ({log.length})</div>
                        <div className="timeSort">시간순</div>
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
                        {log.map((item, index) => (
                            <div className="logBox">
                                <div className="logTitle">
                                    {formatLog(item.start_time)} TASK {item.get_id}
                                </div>
                                <div className="logScore">총 수거량 : {item.laundry_cnt}</div>
                                <div className="logTime">{formatLog(item.start_time)} ~ {formatLog(item.end_time)}</div>
                            </div>
                        
                        ))}
                        {/* <div className="logBox">
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
                            
                        </div> */}
                    </div>
                }
                
        </div> 
    );
};

export default TurtleBotLog;
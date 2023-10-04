import React,{ useEffect, useState } from "react";
import "./style.css";
import { defaultInstance as api } from '../../util/token';
import { useNavigate } from "react-router-dom";

const TurtleBotLog = () =>{
    const navigate = useNavigate();

    const GoMain = () => {
        navigate("/main");
    };

    const [logprogress, setLogprogress] = useState();
    const [log, setLog] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(()=>{
        getLog();
    },[]);
    const getLog = () => {
        api.get("/log?id="+localStorage.getItem("userId"))
        .then((res)=>{
            console.log(res);
            setLog(res.data.log);
            if(res.data.log_in_progress != null){
                setLogprogress(res.data.log_in_progress);
            }
            setLoading(false);
        }).catch((err)=>{
            window.alert("로그를 불러오는 중 문제가 발생했습니다.");
        })
    };
    const formatLog = (value) => {
        return value.split('T')[1];
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
                <div className = "areah-90">
                    <div className="areah-100 justalign-center">
                        <div className = "schdulebox">
                            <div className = "areah-10 justalign-center">
                                <div className = "areaw-20 justalign-center fontchange">동작 기록 ({logprogress != null? log.length+1:log.length})</div>
                                <div className = "areaw-60"></div>
                                <div className = "areaw-20 justalign-center fontchange">시간순</div>
                            </div>

                            {logprogress ? (
                                <div className="logBox">
                                    <div className = "areah-15 colora logTitle">{logprogress.get_name}</div>
                                    <div className = "areah-15 logsubTitle">예상시간 : {logprogress.expected_time}분</div>
                                    <div className = "areah-50 justalign-center">
                                        <div className = "areaw-40 justalign-center clothsd" >
                                            진행중입니다...
                                        </div>
                                        <div className = "areaw-20 justalign-center clothsd" >
                                        </div>
                                        <div className = "areaw-30 justalign-center clothsd">
                                            <div className="justalign-center">
                                                <img className="loading-logo" src={`/loading_resize.gif`} />
                                            </div>
                                        </div>
                                    </div>
                                    <div className = "areah-20 justalign-center">
                                        <div className = "areaw-40 justalign-center">{formatLog(logprogress.start_time)} - ??</div>
                                        <div className = "areaw-20"></div>
                                        <div className = "areaw-40 justalign-center"></div>
                                    </div>
                                </div>
                            ) : null}
                            {log.map((item, index) => (
                                <div className="logBox">
                                    <div className = "areah-15 colorb logTitle">{item.get_name}</div>
                                    <div className = "areah-15 logsubTitle">총 수거량 : {item.laundry_cnt}</div>
                                    <div className = "areah-50 justalign-center">
                                        <div className = "areaw-30 justalign-center clothsd" >
                                            <div className="star-logoframe justalign-center">
                                                <img className="star-logo" src={`/star-shirts.png`} />
                                            </div>
                                            {item.laundries[0].cnt}개
                                        </div>
                                        <div className = "areaw-30 justalign-center clothsd">
                                            <div className="star-logoframe justalign-center">
                                                <img className="star-logo" src={`/star-pants.png`} />
                                            </div>
                                            {item.laundries[1].cnt}개
                                        </div>
                                        <div className = "areaw-30 justalign-center clothsd">
                                            <div className="star-logoframe justalign-center">
                                                <img className="star-logo" src={`/star-towel.png`} />
                                            </div>
                                            0개
                                        </div>
                                    </div>
                                    <div className = "areah-20 justalign-center">
                                        <div className = "areaw-40 justalign-center">{formatLog(item.start_time)} - {formatLog(item.end_time)}</div>
                                        <div className = "areaw-20"></div>
                                        <div className = "areaw-40 justalign-center">총 가동시간 : {item.total_time}분</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            }
        </div> 
    );
};

export default TurtleBotLog;
import React, { useState } from "react";
import "./ScheduleStyle.css";
import { Form, useNavigate } from "react-router-dom";

const AddSchedule = () => {
    const [hourValue, setHourValue] = useState(12);
    const [minuteValue, setMinuteValue] = useState(0);
    const [meridiemValue, setMeridiemValue] = useState('PM');

    const [isMon, setIsMon] = useState(false);
    const [isTue, setIsTue] = useState(false);
    const [isWed, setIsWed] = useState(false);
    // const [isMon, setIsMon] = useState(false);
    // const [isMon, setIsMon] = useState(false);
    // const [isMon, setIsMon] = useState(false);
    // const [isMon, setIsMon] = useState(false);

    const formatHour = (value) => {
        return value.toLocaleString(undefined, { minimumIntegerDigits: 2 });
    };
    const addhour = (e) => {
        e.preventDefault()
        if (hourValue == 23){
            setHourValue(1);
        }else{
            setHourValue(hourValue + 2);
        }
    };
    const decreasehour = (e) => {
        e.preventDefault()
        if (hourValue == 0 || hourValue == 1){
            setHourValue(23);
        }else{
            setHourValue(hourValue - 2);
        }
    };

    return(
    <>
        <div style={{position:'absolute',width:'390px', height:'812px'}}>
            <div style={{width:'100%', height:'20%'}}>
                <div style={{width:'100%', height:'40%', display:'flex', justifyContent:'center',alignItems:'center'}}>
                    <div style={{width:'20%', height:'100%', display:'flex', justifyContent:'center',alignItems:'center'}}>‹</div>
                    <div style={{width:'80%', height:'100%', display:'flex', justifyContent:'center',alignItems:'center'}}>터틀봇 제어</div>
                    <div style={{width:'20%', height:'100%', display:'flex', justifyContent:'center',alignItems:'center'}}>🏠</div>
                </div>
                <div style={{width:'100%', height:'60%', display:'flex', justifyContent:'flex-start',alignItems:'center'}}>
                    <div style={{marginLeft:'30px'}}>스케줄 추가</div>
                </div>
            </div>
            <form style={{width:'100%', height:'80%'}}>
                <div style={{width:'100%', height:'75%'}}>
                    <div style={{width:'100%', height:'25%', display:'flex', justifyContent:'center',alignItems:'center'}}>
                        <div>
                            <label for="title">제목</label><br/>
                            <input type="text" id="title" name="title" placeholder="title" required/>
                        </div>
                    </div>
                    <div style={{width:'100%', height:'55%', display:'flex', justifyContent:'center',alignItems:'center'}}>
                        <div>
                            <div style={{color:'#838589'}}>시간</div><br/>
                            <div style={{width:'325px', height:'200px',border:'1px solid #ededed',backgroundColor:'#fafafa', borderRadius:'10px', display:'flex', justifyContent:'center',alignItems:'center'}}>
                                <div style={{width:'30%', height:'100%'}}>
                                    <div style={{width:'100%', height:'33%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'30px',color:'#838589'}} onClick={decreasehour}>{hourValue == 0 || hourValue == 1 ? 23 : formatHour(hourValue - 2)}</div>
                                    <div style={{width:'100%', height:'33%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'30px'}}>{formatHour(hourValue)}</div>
                                    <div style={{width:'100%', height:'33%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'30px',color:'#838589'}} onClick={addhour}>{hourValue === 23 ? formatHour(0) : formatHour(hourValue + 2)}</div>
                                </div>
                                <div style={{width:'10%', height:'100%'}}>
                                    <div style={{width:'100%', height:'33%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'30px',color:'#838589'}}></div>
                                    <div style={{width:'100%', height:'33%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'30px'}}>:</div>
                                    <div style={{width:'100%', height:'33%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'30px',color:'#838589'}}></div>
                                </div>
                                <div style={{width:'30%', height:'100%'}}>
                                    <div style={{width:'100%', height:'33%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'30px',color:'#838589'}}>{formatHour(minuteValue) === formatHour(0) ? 59 : formatHour(minuteValue - 1)}</div>
                                    <div style={{width:'100%', height:'33%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'30px'}}>{formatHour(minuteValue)}</div>
                                    <div style={{width:'100%', height:'33%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'30px',color:'#838589'}}>{formatHour(minuteValue) === 59 ? formatHour(0) : formatHour(minuteValue + 1)}</div>
                                </div>
                                <div style={{width:'30%', height:'100%'}}>
                                    <div style={{width:'100%', height:'33%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'30px',color:'#838589'}}>{meridiemValue === 'AM' ? '' : 'AM'}</div>
                                    <div style={{width:'100%', height:'33%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'30px'}}>{meridiemValue}</div>
                                    <div style={{width:'100%', height:'33%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'30px',color:'#838589'}}>{meridiemValue === 'PM' ? '' : 'PM'}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div style={{width:'100%', height:'20%', display:'flex', justifyContent:'center',alignItems:'center'}}>
                        <div>
                            <div style={{color:'#838589',marginLeft:'20px'}}>요일</div><br/>
                            <div style={{width:'360px', height:'50px',border:'1px solid #ededed',backgroundColor:'#fafafa', borderRadius:'10px', display:'flex', justifyContent:'space-evenly',alignItems:'center'}}>
                                <div style={{width:'40px', height:'40px',border:'1px solid #FF9900', borderRadius:'50%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'12px',backgroundColor:'#FF9900',color:'white'}}>Mon</div>
                                <div style={{width:'40px', height:'40px',border:'1px solid #ededed', borderRadius:'50%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'12px',backgroundColor:'#ededed',color:'#838589'}}>Tue</div>
                                <div style={{width:'40px', height:'40px',border:'1px solid #ededed', borderRadius:'50%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'12px',backgroundColor:'#ededed',color:'#838589'}}>Wed</div>
                                <div style={{width:'40px', height:'40px',border:'1px solid #FF9900', borderRadius:'50%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'12px',backgroundColor:'#FF9900',color:'white'}}>Thu</div>
                                <div style={{width:'40px', height:'40px',border:'1px solid #ededed', borderRadius:'50%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'12px',backgroundColor:'#ededed',color:'#838589'}}>Fri</div>
                                <div style={{width:'40px', height:'40px',border:'1px solid #ededed', borderRadius:'50%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'12px',backgroundColor:'#ededed',color:'#838589'}}>Sat</div>
                                <div style={{width:'40px', height:'40px',border:'1px solid #FF9900', borderRadius:'50%', display:'flex', justifyContent:'center',alignItems:'center',fontSize:'12px',backgroundColor:'#FF9900',color:'white'}}>Sun</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div style={{width:'100%', height:'25%', display:'flex', justifyContent:'center',alignItems:'center'}}>
                    <input type="submit" value="스케줄 추가"/>
                </div>
            </form>
        </div>
    </>
    );
};

export default AddSchedule;
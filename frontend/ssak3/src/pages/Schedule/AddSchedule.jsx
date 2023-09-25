import React, { useState } from "react";
import "./ScheduleStyle.css";
import { Form, useNavigate } from "react-router-dom";

const AddSchedule = () => {
    const [hourValue, setHourValue] = useState('1');

    const addhour = (e) => {
        e.preventDefault()
        setHourValue(e.target.value);
    };
    const dechour = (e) => {
        e.preventDefault()
        setHourValue(e.target.value);
    };

    return(
    <>
        <div style={{position:'absolute',width:'390px', height:'812px',border:'1px solid black'}}>
            <div style={{width:'100%', height:'20%',border:'1px solid red'}}>
                <div style={{width:'100%', height:'40%',border:'1px solid blue', display:'flex', justifyContent:'center',alignItems:'center'}}>
                    <div style={{width:'20%', height:'100%',border:'1px solid blue', display:'flex', justifyContent:'center',alignItems:'center'}}>‹</div>
                    <div style={{width:'80%', height:'100%',border:'1px solid blue', display:'flex', justifyContent:'center',alignItems:'center'}}>터틀봇 제어</div>
                    <div style={{width:'20%', height:'100%',border:'1px solid blue', display:'flex', justifyContent:'center',alignItems:'center'}}>🏠</div>
                </div>
                <div style={{width:'100%', height:'60%',border:'1px solid blue', display:'flex', justifyContent:'flex-start',alignItems:'center'}}>
                    <div style={{marginLeft:'30px',border:'1px solid blue'}}>스케줄 추가</div>
                </div>
            </div>
            <form style={{width:'100%', height:'80%',border:'1px solid red'}}>
                <div style={{width:'100%', height:'75%',border:'1px solid red'}}>
                    <div style={{width:'100%', height:'25%',border:'1px solid blue', display:'flex', justifyContent:'center',alignItems:'center'}}>
                        <div>
                            <label for="title">제목</label><br/>
                            <input type="text" id="title" name="title" placeholder="title" required/>
                        </div>
                    </div>
                    <div style={{width:'100%', height:'55%',border:'1px solid blue', display:'flex', justifyContent:'center',alignItems:'center'}}>
                        <div>
                            <div style={{color:'#838589'}}>시간</div><br/>
                            <div style={{width:'325px', height:'200px',border:'1px solid #ededed',backgroundColor:'#fafafa', borderRadius:'10px', display:'flex', justifyContent:'center',alignItems:'center'}}>
                                <div style={{width:'30%', height:'100%',border:'1px solid red'}}>
                                    <div style={{width:'100%', height:'33%',border:'1px solid red'}}>{hourValue - 1}</div>
                                    <div style={{width:'100%', height:'33%',border:'1px solid red'}}>{hourValue}</div>
                                    <div style={{width:'100%', height:'33%',border:'1px solid red'}}>{hourValue + 1}</div>
                                </div>
                                <div style={{width:'10%', height:'100%',border:'1px solid red'}}>
                                    ⁚
                                </div>
                                <div style={{width:'30%', height:'100%',border:'1px solid red'}}>
                                    <div style={{width:'100%', height:'33%',border:'1px solid red'}}>{hourValue - 1}</div>
                                    <div style={{width:'100%', height:'33%',border:'1px solid red'}}>{hourValue}</div>
                                    <div style={{width:'100%', height:'33%',border:'1px solid red'}}>{hourValue + 1}</div>
                                </div>
                                <div style={{width:'30%', height:'100%',border:'1px solid red'}}>
                                    <div style={{width:'100%', height:'33%',border:'1px solid red'}}>{hourValue - 1}</div>
                                    <div style={{width:'100%', height:'33%',border:'1px solid red'}}>{hourValue}</div>
                                    <div style={{width:'100%', height:'33%',border:'1px solid red'}}>{hourValue + 1}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div style={{width:'100%', height:'20%',border:'1px solid blue'}}>
                        요일
                    </div>
                </div>
                <div style={{width:'100%', height:'25%',border:'1px solid red', display:'flex', justifyContent:'center',alignItems:'center'}}>
                    <input type="submit" value="스케줄 추가"/>
                </div>
            </form>
        </div>
    </>
    );
};

export default AddSchedule;
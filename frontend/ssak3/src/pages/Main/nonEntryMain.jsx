import React from "react";
import { useNavigate } from "react-router-dom";
import "./Main.css";

const NonEntryMain = ( ) =>{
    const navigate = useNavigate();

    const GoRegister = () => {
        navigate("/addturtle");
    };

    return (
        <div className="main-container">
            <div className = "areah-60">
                <div className = "addturtle-title">TurtleBot - 미등록</div>
                <div className = "areah-45">
                    <div className = "nonturtle-image"></div>
                </div>
                <div className = "areah-30">
                    <div className = "areah-50 justalign-center">연결된 기기가 없습니다.</div>
                    <div className = "areah-50 justalign-center"></div>
                </div>
            </div>
            <div className = "areah-40">
                <div onClick={GoRegister} style={{width:'100%',height:'35%',display:'flex',justifyContent:'center',alignItems:'center',cursor:'pointer'}}>
                    <div style={{width:'60%',height:'50%',display:'flex',justifyContent:'center',alignItems:'center',fontSize:'25px',color:'#838589'}}>기기 등록하기</div>
                    <div style={{width:'20%',height:'50%',display:'flex',justifyContent:'center',alignItems:'center',fontSize:'25px',color:'#838589'}}>›</div>
                </div>
                <div style={{width:'90%',height:'1%',borderBottom:'2px solid #ededed',marginLeft:'5%'}}></div>
                <div style={{width:'100%',height:'35%',display:'flex',justifyContent:'center',alignItems:'center'}}>
                    <div style={{width:'60%',height:'50%',display:'flex',justifyContent:'flex-start',alignItems:'center',fontSize:'25px',color:'#838589'}}>초기화면으로 돌아가기</div>
                    <div style={{width:'20%',height:'50%',display:'flex',justifyContent:'center',alignItems:'center',fontSize:'25px',color:'#838589'}}>›</div>
                </div>
                <div style={{width:'90%',height:'1%',borderBottom:'2px solid #ededed',marginLeft:'5%'}}></div>
            </div>
        </div>
    );
};

export default NonEntryMain;
import React from "react";
import "./Main.css";
import { useNavigate } from "react-router-dom";

const EntryMain = ( ) =>{
    const navigate = useNavigate();

    const GoControl = () => {
        navigate("/start");
    };

    const GoLog = () => {
        navigate("/log");
    };

    const GoSchedule = () => {
        navigate("/schedule");
    };

    const handleLogout = () => {
        localStorage.removeItem('userId');
        localStorage.removeItem('accessToken');
        localStorage.removeItem('turtlebot');
        navigate("/");
    };

    let name = localStorage.getItem('turtlebot');

    return (
    <div className="main-container">
        <div className = "areah-40">
            <div className = "turtle-title">{name}</div>
            <div className = "areah-55">
                <div className = "addturtle-image"></div>
            </div>
        </div>
        <div className="areah-60 justalign">
            <div onClick={GoControl} className = "turtle-button justalign-center">
                <div className = "turtle-index justalign-center">
                    <div className = "areah-50">터틀봇 제어</div>
                    <div className = "areah-50 turtle-buttonc">작동 상태 확인</div>
                </div>
                <div className = "turtle-indexb justalign-center">›</div>
            </div>
            <div className = "nonturtle-underline"></div>
            <div onClick={GoLog} className = "turtle-button justalign-center">
                <div className = "turtle-index justalign-center">
                    <div className = "areah-50">사용 기록</div>
                    <div className = "areah-50 turtle-buttonc">최근 사용 목록</div>
                </div>
                <div className = "turtle-indexb justalign-center">›</div>
            </div>
            <div className = "nonturtle-underline"></div>
            <div onClick={GoSchedule} className = "turtle-button justalign-center">
                <div className = "turtle-index justalign-center">
                    <div className = "areah-50">시간 설정</div>
                    <div className = "areah-50 turtle-buttonc">시간 및 요일 설정</div>
                </div>
                <div className = "turtle-indexb justalign-center">›</div>
            </div>
            <div className = "nonturtle-underline"></div>
            <div onClick={handleLogout} className = "turtle-button justalign-center">
                <div className = "turtle-index justalign-center">
                    <div className = "areah-50">초기화면으로 돌아가기</div>
                    <div className = "areah-50 turtle-buttonc">로그아웃</div>
                </div>
                <div className = "turtle-indexb justalign-center">›</div>
            </div>
        </div>
    </div>
    );
};

export default EntryMain;
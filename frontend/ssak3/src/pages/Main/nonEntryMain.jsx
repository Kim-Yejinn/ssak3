import React from "react";
import { useNavigate } from "react-router-dom";
import "./Main.css";

const NonEntryMain = ( ) =>{
    const navigate = useNavigate();

    const GoRegister = () => {
        navigate("/addturtle");
    };

    const handleLogout = () => {
        localStorage.removeItem('userId');
        localStorage.removeItem('accessToken');
        localStorage.removeItem('turtlebot');
        navigate("/");
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
                <div onClick={GoRegister} className = "nonturtle-button justalign-center">
                    <div className = "nonturtle-index justalign-center">기기 등록하기</div>
                    <div className = "nonturtle-indexb justalign-center">›</div>
                </div>
                <div className = "nonturtle-underline"></div>
                <div onClick={handleLogout} className = "nonturtle-button justalign-center">
                    <div className = "nonturtle-index justalign-center">초기화면으로 돌아가기</div>
                    <div className = "nonturtle-indexb justalign-center">›</div>
                </div>
                <div className = "nonturtle-underline"></div>
            </div>
        </div>
    );
};

export default NonEntryMain;
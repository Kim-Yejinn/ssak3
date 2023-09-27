import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Cookies } from 'react-cookie';
import { defaultInstance as api } from '../../util/token.jsx';
import "./Main.css";

const AddTuttle = () => {
    const navigate = useNavigate();

    const GoMain = () => {
        navigate("/main");
    };

    const [inputTurtle, setInputTurtle] = useState('');

    const handleInputChange = (event) => {
        setInputTurtle(event.target.value);
    };

    const formdata = {
        "id" : "test1234",
        "serial_number" : inputTurtle
    }

    const sendRegister = async (event) => {
        event.preventDefault();
        try {
            const response = await api.post("/robot/regist", formdata);
            console.log('등록성공', response.data);
            navigate('/main');
        } catch (error) {
            console.error(error);
            setInputTurtle('');
            alert("오류가 발생했습니다.");
        }
    };

    return(
        <div className = "main-container">
            <div className = "areah-60">
                <div className = "addturtle-title">기기 등록</div>
                <div className = "areah-45">
                    <div className = "addturtle-image"></div>
                </div>
                <div className = "areah-30">
                    <div className = "areah-50 justalign-center">↑</div>
                    <div className = "areah-50 justalign-center">기기 하단의 시리얼 넘버를 입력해 주세요.</div>
                </div>
            </div>
            <div className = "areah-40">
                <div className = "areah-50 justalign-center">
                    <input type="text" value={inputTurtle} onChange={handleInputChange} placeholder="Serial Number" required/>
                </div>
                <div className = "addturtle-submit">
                    <div className = "addturtle-buttonarea">
                        <div onClick={GoMain} className = "addturtle-button">취소</div>
                        <div onClick={sendRegister} className = "addturtle-button">등록하기</div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default AddTuttle;
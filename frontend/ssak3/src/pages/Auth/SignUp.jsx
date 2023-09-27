import React, { useRef } from "react";
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import "./LoginStyles.css";

const SignUp = ( ) =>{
    const instance = axios.create({
        baseURL: 'https://j9b201.p.ssafy.io/api',
        headers: { 'Content-type': 'application/json' },
    });
    const nameRef = useRef();
    const idRef = useRef();
    const passwordRef = useRef();
    
    const navigate = useNavigate();
    
    const onSubmit = async (e) => {
        console.log(e.data);
        try{
            const res = await instance.post('/auth/sign-up', 
            {
                "name" : nameRef.current.value,
                "id" : idRef.current.value,
                "password" : passwordRef.current.value
            });
            console.log('회원가입 성공!', res.data);
            navigate('/');

        } catch(err){
            window.alert("회원가입 실패 : "+err);
        }
    }
    return (
    <div className="container">
        <div className="signupheader">
            <p className="signupTitle">회원가입</p>
            <p className="signupTitleLabel">회원정보를 입력하세요</p>
        </div>
        <div className="signupForm">
            <div className="signupFormarea">
                <div>
                    <label for="username">이름</label><br/>
                    <input type="text"placeholder="name" ref={nameRef} required/>
                </div>
                <div>
                    <label for="userid">아이디</label><br/>
                    <input type="text" placeholder="ID" ref={idRef} required/>
                </div>
                <div>
                    <label for="password">비밀번호</label><br/>
                    <input type="password" placeholder="Password" ref={passwordRef} required/>
                    <p>비밀번호는 반드시 6자 이상이어야 합니다.</p>
                </div>
            </div>
            <div className="signupFormsubmit">
                <button className="formSubmit" onClick={onSubmit}>가입하기</button>
            </div>
        </div>
    </div>
    );
};

export default SignUp;
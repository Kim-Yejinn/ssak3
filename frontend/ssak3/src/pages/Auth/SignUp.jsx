import React, {useState} from "react";
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import "./LoginStyles.css";

const SignUp = ( ) =>{
    const instance = axios.create({
        baseURL: 'https://j9b201.p.ssafy.io:8080',
        headers: { 'Content-type': 'application/json' },
    });
    const navigate = useNavigate();
    const [formData, setFormData] = useState(
        {
            id: '',
            name: '',
            password: ''
        }
    );
    const onSubmit = async (e) => {
        console.log(e.data);
        try{
            const res = await instance.post('/auth/sign-up', formData);
            console.log('회원가입 성공!', res.data);
            navigate('/');

        } catch(err){
            window.alert("회원가입 실패 : "+err);
        }
    }
    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData({ ...formData, [name]: value});
    };
    return (
    <div className="container">
        <div className="signupheader">
            <p className="signupTitle">회원가입</p>
            <p className="signupTitleLabel">회원정보를 입력하세요</p>
        </div>
        <form method="post" className="signupForm" onSubmit={onSubmit}>
            <div className="signupFormarea">
                <div>
                    <label for="username">이름</label><br/>
                    <input type="text" id="name" name="name" placeholder="name" onChange={handleChange} required/>
                </div>
                <div>
                    <label for="userid">아이디</label><br/>
                    <input type="text" id="id" name="id" placeholder="ID" onChange={handleChange} required/>
                </div>
                <div>
                    <label for="password">비밀번호</label><br/>
                    <input type="password" id="password" name="password" placeholder="Password" onChange={handleChange} required/>
                    <p>비밀번호는 반드시 6자 이상이어야 합니다.</p>
                </div>
            </div>
            <div className="signupFormsubmit">
                <input type="submit" value="가입하기" />
            </div>
        </form>
    </div>
    );
};

export default SignUp;
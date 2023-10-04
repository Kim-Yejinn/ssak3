import React, {useRef} from "react";
import "./LoginStyles.css";
import { useNavigate } from "react-router-dom";
import { defaultInstance as api } from '../../util/token';

const Login = () =>{
    const userIdRef = useRef();
    const passwordRef = useRef();
    const navigate = useNavigate();

    const GoSignUp = () => {
        navigate("/signup");
    };

    const login = () => {
        api.post("/auth/log-in", {
            'id' : userIdRef.current.value,
            'password' : passwordRef.current.value
        })
       .then((res)=>{
            console.log(res.data);
            localStorage.setItem('accessToken',res.data.accessToken);
            localStorage.setItem('userId',userIdRef.current.value);
            navigate("/main");
       })
        .catch((err)=>{
            window.alert("아이디나 비밀번호를 확인해주세요.");
       });
    }
    
    return (
    <div className="container">
        <div className="main">
            <div className="mainImage">
                <div style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/tuttle.png)`,width:'100%', height: '100%',backgroundSize:'cover'}}></div>
            </div>
            <div className="mainTitle">
                싹쓸이
            </div>
        </div>
        <div className="formarea" >
            <div className="formarea">
                <input type="text" ref={userIdRef} placeholder="ID" required/>
                <input type="password" ref={passwordRef} placeholder="Password" required/>
            </div>
            <div className="formsubmit">
                <button className="formSubmit" onClick={login}>로그인 </button>
                <p>계정이 없으십니까?&nbsp; <a onClick={GoSignUp}>회원가입</a></p>
            </div>
        </div>
    </div>
    );
};

export default Login;
import React from "react";
import styles from "./LoginStyles.css";
import { useNavigate } from "react-router-dom";

const Login = ( ) =>{
    const navigate = useNavigate();

    const GoSignUp = () => {
        navigate("/signup");
    };

    return (
    <div className="container">
        <div className="main">
            {/* <div className="emptySpace"></div> */}
            <div className="mainImage">
                <div style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/tuttle.png)`,width:'100%', height: '100%',backgroundSize:'cover'}}></div>
            </div>
            <div className="mainTitle">
                싹쓰리
            </div>
        </div>
        <form className="formarea">
            <div className="formarea">
                <input type="text" id="username" name="username" placeholder="ID" required/>
                <input type="password" id="password" name="password" placeholder="Password" required/>
            </div>
            <div className="formsubmit">
                <input type="submit" value="로그인"/>
                <p>계정이 없으십니까?&nbsp; <a onClick={GoSignUp}>회원가입</a></p>
            </div>
        </form>
    </div>
    );
};

export default Login;
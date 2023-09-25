import React from "react";
import "./LoginStyles.css";

const SignUp = ( ) =>{
    return (
    <div className="container">
        <div className="signupheader">
            <p className="signupTitle">회원가입</p>
            <p className="signupTitleLabel">회원정보를 입력하세요</p>
        </div>
        <form className="signupForm">
            <div className="signupFormarea">
                <div>
                    <label for="username">이름</label><br/>
                    <input type="text" id="username" name="username" placeholder="name" required/>
                </div>
                <div>
                    <label for="userid">아이디</label><br/>
                    <input type="text" id="userid" name="userid" placeholder="ID" required/>
                </div>
                <div>
                    <label for="password">비밀번호</label><br/>
                    <input type="password" id="password" name="password" placeholder="Password" required/>
                    <p>비밀번호는 반드시 6자 이상이어야 합니다.</p>
                </div>
            </div>
            <div className="signupFormsubmit">
                <input type="submit" value="가입하기"/>
            </div>
        </form>
    </div>
    );
};

export default SignUp;
import React from "react";

import styles from "../LoginStyles.css";

const SignUp = ( ) =>{
    return (
    <div className="container" style={{border:'1px solid red'}}>
        <div style={{width: '100%', height: '30%', border:'solid 1px red', display:'flex',textAlign:'left',alignItems:'center',flexDirection:'column'}}>
            <p style={{fontSize:'30px'}}>회원가입</p>
            <p>회원정보를 입력하세요</p>
        </div>
        <div style={{width: '100%', height: '50%', border:'solid 1px red'}}></div>
        <div style={{width: '100%', height: '20%', border:'solid 1px red'}}></div>
    </div>
    );
};

export default SignUp;
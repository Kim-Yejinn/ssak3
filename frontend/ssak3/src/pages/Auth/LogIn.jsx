import React, {useState} from "react";
import "./LoginStyles.css";
import { useNavigate } from "react-router-dom";
// import { defaultInstance as api } from '../../util/token';

const Login = ( ) =>{

    const [formData, setFormData] = useState({
        "id" : "",
        "password" : ""
    });
    const navigate = useNavigate();

    const GoSignUp = () => {
        navigate("/signup");
    };


    // const login = () => {
    //     api.post("/log-in", formData)
    //    .then((res)=>{
    //         navigate("/main");
    //    })
    //     .catch((err)=>{

//        });
    // }
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
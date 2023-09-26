import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Cookies } from 'react-cookie';
import { defaultInstance as api } from '../../util/token.jsx';

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
        "id" : "test",
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
        <>
            <div style={{position:'absolute',width:'390px', height:'812px'}}>
                <div style={{width:'100%', height: '60%'}}>
                    <div style={{width:'100%',height:'20%', display:'flex', justifyContent:'center',alignItems:'end',fontSize:'30px',marginBottom:'5%'}}>기기 등록</div>
                    <div style={{width:'100%',height:'45%'}}>
                        <div style={{backgroundImage: `url(${process.env.PUBLIC_URL}/turtlebotImage.png)`,width:'50%', height: '100%',backgroundSize:'cover',marginLeft:'22%'}}></div>
                    </div>
                    <div style={{width:'100%',height:'30%'}}>
                        <div style={{width:'100%',height:'50%', display:'flex', justifyContent:'center',alignItems:'center'}}>↑</div>
                        <div style={{width:'100%',height:'50%', display:'flex', justifyContent:'center',alignItems:'center'}}>기기 하단의 시리얼 넘버를 입력해 주세요.</div>
                    </div>
                </div>
                <div style={{width:'100%', height: '40%'}}>
                    <div style={{width:'100%', height: '50%', display:'flex', justifyContent:'center',alignItems:'center'}}>
                        <input type="text" value={inputTurtle} onChange={handleInputChange} placeholder="Serial Number" required/>
                    </div>
                    <div style={{width:'100%', height: '50%', display:'flex', justifyContent:'center',alignItems:'start'}}>
                        <div style={{width:'325px', height: '30%',display:'flex', justifyContent:'space-between'}}>
                            <div onClick={GoMain} style={{width:'150px', height: '50px',border:'1px solid #ededed', display:'flex', justifyContent:'center',alignItems:'center',backgroundColor:'#fafafa', borderRadius:'10px',fontFamily:'inherit',color:'#838589', cursor:'pointer'}}>취소</div>
                            <div onClick={sendRegister} style={{width:'150px', height: '50px',border:'1px solid #ededed', display:'flex', justifyContent:'center',alignItems:'center',backgroundColor:'#fafafa', borderRadius:'10px',fontFamily:'inherit',color:'#838589', cursor:'pointer'}}>등록하기</div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}

export default AddTuttle;
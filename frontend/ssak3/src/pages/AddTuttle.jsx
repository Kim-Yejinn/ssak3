import React from "react";


const AddTuttle = () => {
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
                        <input type="text" id="serial" name="serial" placeholder="Serial Number" required/>
                    </div>
                    <div style={{width:'100%', height: '50%', display:'flex', justifyContent:'center',alignItems:'start'}}>
                        <div style={{width:'325px', height: '30%',display:'flex', justifyContent:'space-between'}}>
                            <button style={{width:'150px', height: '50px',border:'1px solid #ededed',backgroundColor:'#fafafa', borderRadius:'10px',fontFamily:'inherit',color:'#838589'}}>취소</button>
                            <button style={{width:'150px', height: '50px',border:'1px solid #ededed',backgroundColor:'#fafafa', borderRadius:'10px',fontFamily:'inherit',color:'#838589'}}>등록하기</button>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}

export default AddTuttle;
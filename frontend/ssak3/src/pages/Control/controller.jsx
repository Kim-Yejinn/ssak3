import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './style.css';
import { defaultInstance as api } from '../../util/token';

const Controller = () => {
    let clothes = ["셔츠", "바지", "수건","양말", "속옷",];
    let clothesLogo = ["shirts.png", "pants.png","towel.png","socks.png","underwear.png"];
    const [loading, setLoading] = useState(true);
    const [frames, setFrames] = useState([false,false,false,false,false]);
    const [toggles, setToggles] = useState([false,false,false,false,false]);
    const userId = localStorage.getItem('userId');

    const starRequest = (index) => {
        const url = "https://j9b201.p.ssafy.io/api/dib";
        if(!frames[index]){
            axios.post(url,{
                "user_id" : userId,
                "laundry_id" : index+1
            })
            .then(response => {
                console.log("success : ",response.data);
            })
            .catch(error => {
                console.log("failed : ",error);
            });
            starSetter(index);
        }else{
            axios.delete(url+"/"+(index+1)+"?user_id="+userId)
            .then(response => {
                console.log("success : ",response.data);
            })
            .catch(error => {
                console.log("failed : ",error);
            });
            starSetter(index);
        }
    };
    const starSetter = (index) => {
        const updatedFrames = [...frames];
        updatedFrames[index] = !updatedFrames[index];
        const updatedToggles = [...toggles];
        updatedToggles[index] = true;
        setFrames(updatedFrames);
        setToggles(updatedToggles);
    };
    const toggleSetter = (index) => {
        const updatedToggles = [...toggles];
        updatedToggles[index] = !updatedToggles[index];
        setToggles(updatedToggles);
    };
    useEffect(() => {
        const url = "/dib/list?id=" + userId
        api.get(url)
        .then(response => {
            const setting = [false,false,false,false,false];
            for(let i=0;i<5;i++){
                console.log(response.data[i].is_dib);
                if(response.data[i].is_dib){
                    setting[i] = true;
                }
            }
            setFrames(setting);
            setToggles(setting);
        })
        .then(()=>{
            setLoading(false);
        })
        .catch(error => {
            console.error('에러 발생:', error);
        });
        
    }, [userId,]);
    
    const robotRequest = () => {
        // 
        let list = [];
        for(let i=0;i<5;i++)
            if(toggles[i]) list.push(i+1);
        // request
        api.post("/run/start", {
            "id" : userId,
            "laundryList" : list
        })
        .then((response) => {
            alert("OK : ",response.data);
        })
        .catch((error) => {
            alert("Error : ", error);
        })
    }
    return (
        <div>
        {
        loading ?
        <div className="logContainer">
             <div className="axiosLoadingGif"> </div>
        </div>
        :
        <div className="frameContainer">
            {
                frames.map((item,index) => (
                        item ?
                        <div className="starFrame" key={index}>
                            <div className="starLogoFrame">
                                <img className="starLogo" src={`/star-${clothesLogo[index]}`} />
                            </div>
                            <div className="starBtn" onClick={() => starRequest(index)}></div>
                            <div className="starTitle">{clothes[index]}</div>
                            { toggles[index] ?
                            <div>
                                <div className="starOnText">On</div>
                                <div className="starToggleOnBg" onClick={() => toggleSetter(index)}>
                                    <div className="starToggleOn" onClick={() => toggleSetter(index)}></div>
                                </div>
                            </div>
                            :
                            <div>
                                <div className="offText">Off</div>
                                <div className="starToggleOffBg" onClick={() => toggleSetter(index)}>
                                    <div className="starToggleOff" onClick={() => toggleSetter(index)}></div>
                                </div>
                            </div>
                            }
                        </div>
                        :
                        <div className="unstarFrame" key={index}>
                            <div className="logoFrame">
                                <img className="unstarLogo" src={`/${clothesLogo[index]}`} />
                            </div>
                            <div className="unStarBtn" onClick={() => starRequest(index)}></div>
                            <div className="unstarTitle">{clothes[index]}</div>
                            { toggles[index] ?
                            <div>
                                <div className="unstarOnText">On</div>
                                <div className="toggleOnBg" onClick={() => toggleSetter(index)}>
                                    <div className="toggleOn" onClick={() => toggleSetter(index)}></div>
                                </div>
                            </div>
                            :
                            <div>
                                <div className="offText">Off</div>
                                <div className="toggleOffBg" onClick={() => toggleSetter(index)}>
                                    <div className="toggleOff" onClick={() => toggleSetter(index)}></div>
                                </div>
                            </div>
                            }
                        </div>
                ))
            }
                
            <button className="startBtn" onClick={robotRequest}>
                주행하기
            </button>
        </div>
}
</div>
);
}

export default Controller;
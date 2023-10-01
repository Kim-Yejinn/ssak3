import React, { useState } from 'react';
import axios from 'axios';
import './style.css';

const Controller = () => {
    let clothes = ["셔츠", "바지", "수건","양말", "속옷",];
    const [frames, setFrames] = useState([true,true,true,true,true]);
    const [toggles, setToggles] = useState([true, false,false,false,false]);
    const starSetter = (index) => {
        const updatedFrames = [...frames];
        updatedFrames[index] = !updatedFrames[index];
        setFrames(updatedFrames);
    }
    const toggleSetter = (index) => {
        const updatedToggles = [...toggles];
        updatedToggles[index] = !updatedToggles[index];
        setToggles(updatedToggles);
    };
    const [requestDto, setRequestDto] = useState({
        "memberId" : 1,
        "laundry" : ["shirts", "pants"],
        "time" : 13
    });
    
    const robotRequest = (e) => {
        // e.preventDefault();

        // request
        axios.post("", requestDto)
        .then((response) => {
            alert("OK : ",response.data);
        })
        .catch((error) => {
            alert("Error : ", error);
        })
    }
    return (
        <div className="frameContainer">
            {
                frames.map((item,index) => (
                        item ?
                        <div className="starFrame" key={index}>
                            <div className="starLogoFrame"></div>
                            <div className="starBtn" onClick={() => starSetter(index)}></div>
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
                            <div className="logoFrame"></div>
                            <div className="unStarBtn" onClick={() => starSetter(index)}></div>
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
    );

}

export default Controller;
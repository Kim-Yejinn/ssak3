import React, { useState } from 'react';
import axios from 'axios';
import styles from './style.css';

const Controller = () => {
    const [starIsVisible, setStarIsVisible] = useState(false);
    const [isVisible, setIsVisible] = useState(false);
    const starToggleVisibility = () =>{
        setStarIsVisible(!starIsVisible);
    };
    const toggleVisibility = () => {
        setIsVisible(!isVisible);
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
        <div>
            <div className="starFrame">
                    <div className="starLogoFrame"></div>
                    <div className="starBtn"></div>
                    <div className="starTitle">T-shirt</div>
                    { starIsVisible ?
                    <div>
                        <div className="starOnText">On</div>
                        <div className="starToggleOnBg">
                            <div className="starToggleOn" onClick={starToggleVisibility}></div>
                        </div>
                    </div>
                    :
                    <div>
                        <div className="offText">Off</div>
                        <div className="starToggleOffBg">
                            <div className="starToggleOff" onClick={starToggleVisibility}></div>
                        </div>
                    </div>
                    }
                </div>
                <div className="unstarFrame">
                    <div className="logoFrame"></div>
                    <div className="unStarBtn"></div>
                    <div className="unstarTitle">Pants</div>
                    {isVisible ?
                    <div>
                        <div className="unstarOnText">On</div>
                        <div className="toggleOnBg">
                            <div className="toggleOn" onClick={toggleVisibility}></div>
                        </div>
                    </div>
                    :
                    <div>
                        <div className="offText">Off</div>
                        <div className="toggleOffBg">
                            <div className="toggleOff" onClick={toggleVisibility}></div>
                        </div>
                    </div>
                    }

                </div>
                
            <button className="startBtn" onClick={robotRequest}>
                주행하기
            </button>
        </div>
    );

}

export default Controller;
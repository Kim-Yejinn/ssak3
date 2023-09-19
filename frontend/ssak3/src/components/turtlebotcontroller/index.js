import React from "react";
import styles from "./style.css";
const TurtlebotController = ( {} ) =>{
    let name = "TurtleBot - TB230911_1"; 
    // 나중에 이거 GET으로 받아오는 기능으로 변경
    return (
    // Figma : main - 터틀봇 등록돼있는 상태
    // ㄴ controllerContainer : UI
    <div className="controllerContainer" style={styles.controllerContainer}>
        {/* // Figma : main/More - "터틀봇 - 시리얼 넘버"
            // ㄴ turtlebotName : 터틀봇 시리얼넘버와 이름 */}
        <div className="turtlebotName" style={styles.turtlebotName}>{ name }</div>
        
    </div>
    );
};

export default TurtlebotController;
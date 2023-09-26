// import { faRunning } from '@fortawesome/free-solid-svg-icons';
import axios from 'axios';
// import { func } from 'prop-types';
import { Cookies } from 'react-cookie';

const instance = axios.create({
    baseURL: 'https://j9b201.p.ssafy.io/api',
    headers: { 'Content-type': 'application/json' },
});
// Before request
instance.interceptors.request.use(
    function(config){
        const atk = localStorage.getItem('accessToken');

        if(!atk){
            config.headers.Authorization = null;
            return config;
        }
        //로그인 시 발급받은 atk를 헤더에 담아서 request
        config.headers.Authorization = `${atk}`;
        return config;
    },
    function(error){
        return Promise.reject(error);
    }
);

// cookie 생성
const cookies = new Cookies();

// Response
instance.interceptors.response.use(
    function(response){
        console.log("Response OK");
        return response;
    },
    async error => {
        const{
            config, response: {status},
        } = error;
        if(status === 401){
            const originalRequest = config;
            const refreshToken = cookies.get('refreshToken');

            if (refreshToken) {
                const res = await axios.get('https://i9b301.p.ssafy.io/api/auth/token', {
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `${refreshToken}`,
                    },
                });

                const accessToken = res.data.accessToken;
                await localStorage.setItem('accessToken', accessToken);

                originalRequest.headers.Authorization = `${accessToken}`;
                return axios(originalRequest);

            }
        }

        return Promise.reject(error);
    }
);
export const defaultInstance = instance;
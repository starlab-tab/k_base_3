import axios from 'axios'
import router from '@/router'
import context from "@/main";

const back_off = (msg=undefined) => {
    let key = localStorage.getItem("language")
    localStorage.removeItem('language')
    localStorage.removeItem(key)
    router.replace({name:'Bridge'})
}

const handle_error_msg = (msg=undefined) => {

    if (msg) {
        if (msg.constructor === String) {
            context.$dialog.notify.error(msg, {
                position: 'top-right',
            })
        }else if (msg.constructor === Array) {
            for(var text of msg) {
                context.$dialog.notify.error(text, {
                    position: 'top-right',
                    timeout: 0
                })
            }
        }else {
            
        }
    }
}

const errorHandle = (status, msg) => {
    handle_error_msg(msg)
    switch (status) {
        case 400:
            break;
        case 401:
            back_off();
            break;
        case 403:
            back_off();
            break;
        case 404:
            break;
        default:
            
    }
}

var instance = axios.create({
    timeout: 1000 * 120
});

instance.interceptors.request.use(
    config => {
        const key = localStorage.getItem("language")
        const token = localStorage.getItem(key)
        token && (config.headers['Accept-Content'] = 'En ' + token)
        // token && (config.headers.Authorization = 'Bearer ' + token)
        return config
    },
    error => Promise.error(error))


instance.interceptors.response.use(
    
    res => res.status >=200 && res.status < 300 ? Promise.resolve(res) : Promise.reject(res),
    
    error => {
        const {
            response
        } = error
        if (response) {
            errorHandle(response.status, response.data.msg);
            return Promise.reject(response);
        } else {
            if (!window.navigator.onLine) {
                context.$dialog.notify.error('network down', {
                    position: 'top-right',
                    timeout: 3000
                })
                return Promise.reject(error)
            }else {
                context.$dialog.notify.error('request fail', {
                    position: 'top-right',
                    timeout: 3000
                })
                return Promise.reject(error);
            }
            
        }
    })

export default instance

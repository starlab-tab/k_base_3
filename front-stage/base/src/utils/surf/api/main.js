import base from './base'
import axios from '@/utils/surf/http'

const message_prefix = `${base.scout}/message`


const message = {
    get: function(page=1) {
        return axios.get(`${message_prefix}/${page}`)
    },
    post: function(data) {
        return axios.post(`${message_prefix}`, data)
    },
}

const main = {
    message
}


export default main

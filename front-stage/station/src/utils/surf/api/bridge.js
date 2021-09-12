import base from './base'
import axios from '@/utils/surf/http'

const init_prefix = `${base.scout}/init`
const auth_prefix = `${base.scout}/auth`

const bridge = {
    init: function(data) {
        return axios.post(`${init_prefix}`, data)
    },
    init_auth: function(data) {
        return axios.get(`${auth_prefix}/init`, data)
    },
    auth: function(data) {
        return axios.post(`${auth_prefix}`, data)
    },
    de_auth: function() {
        return axios.get(`${auth_prefix}`)
    }
}

export default bridge
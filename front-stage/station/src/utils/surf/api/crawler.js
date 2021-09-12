import base from './base'
import axios from '@/utils/surf/http'

const crawler_prefix = `${base.scout}/crawler`

const crawler = {
    get: function() {
        return axios.get(`${crawler_prefix}`)
    },
    create: function(data) {
        return axios.put(`${crawler_prefix}`, data)
    },
    update: function(data) {
        return axios.patch(`${crawler_prefix}`, data)
    },
    delete: function(id) {
        return axios.delete(`${crawler_prefix}/${id}`)
    },
    active: function(data) {
        return axios.post(`${crawler_prefix}`, data)
    },
    // url_actived: function(data) {
    //     return axios.post(`${crawler_prefix}/url`, data)
    // },
    // text_actived: function() {
    //     return axios.post(`${crawler_prefix}/text`, data)
    // }
}

export default crawler
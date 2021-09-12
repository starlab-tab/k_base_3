import base from './base'
import axios from '@/utils/surf/http'

const post_prefix = `${base.scout}/blog/post`
const album_prefix = `${base.scout}/blog/album`

const post = {
    get: function(page=1) {
        return axios.get(`${post_prefix}/${page}`)
    },
    detail: function(id) {
        return axios.get(`${post_prefix}/detail/${id}`)
    },
    search: function(data) {
        return axios.post(`${post_prefix}/search`, data)
    },
    spell: function(data) {
        return axios.post(`${post_prefix}/detail`, data)
    }
}

const album = {
    get: function(page=1) {
        return axios.get(`${album_prefix}/${page}`)
    },
    posts: function(data) {
        return axios.get(`${album_prefix}/${data.name}/${data.page}`)
    },
    search: function(data) {
        return axios.post(`${album_prefix}/search`, data)
    }
}


const blog = {
    post,
    album
}


export default blog

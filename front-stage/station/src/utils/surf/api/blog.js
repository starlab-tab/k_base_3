import base from './base'
import axios from '@/utils/surf/http'

const blog_prefix = `${base.scout}/blog`

const post_prefix = `${blog_prefix}/post`
const album_prefix = `${blog_prefix}/album`
const image_prefix = `${blog_prefix}/image`

const post = {
    get: function(page=1) {
        return axios.get(`${post_prefix}/${page}`)
    },
    create: function(data) {
        // post.albums = albums
        return axios.put(`${post_prefix}`, data)
    },
    update: function(data) {
        return axios.patch(`${post_prefix}`, data)
    },
    delete: function(id) {
        return axios.delete(`${post_prefix}/${id}`)
    },
    detail: function(id) {
        return axios.get(`${post_prefix}/detail/${id}`)
    },
    search: function(data) {
        return axios.post(`${post_prefix}/search`, data)
    }
}

const album = {
    get: function(page=1) {
        return axios.get(`${album_prefix}/${page}`)
    },
    delete: function(id) {
        return axios.delete(`${album_prefix}/${id}`)
    },
    update: function(data) {
        return axios.patch(`${album_prefix}`, data)
    },
    search: function(data) {
        return axios.post(`${album_prefix}/search`, data)
    }  
}

const image = {
    upload: function(data) {
        return axios.post(`${image_prefix}`, data)
    },
    delete: function(data) {
        return axios.delete(`${image_prefix}`, data)
    },
    als: function(data) {
        return axios.patch(`${image_prefix}`, data)
    }
}


const blog = {
    post,
    album,
    image
}


export default blog

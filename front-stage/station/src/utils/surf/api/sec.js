import base from './base'
import axios from '@/utils/surf/http'

const sec_prefix = `${base.scout}/sec`

const image_prefix = `${sec_prefix}/image`
const archive_prefix = `${sec_prefix}/archive`
const archive_paper_prefix = `${archive_prefix}/paper`
const archive_album_prefix = `${archive_prefix}/album`

const archive = {
    
    paper: {
      get: function(page=1) {
          return axios.get(`${archive_paper_prefix}/${page}`)
      },
      create: function(data) {
          return axios.put(`${archive_paper_prefix}`, data)
      },
      update: function(data) {
          return axios.patch(`${archive_paper_prefix}`, data)
      },
      delete: function(id) {
          return axios.delete(`${archive_paper_prefix}/${id}`)
      },
      detail: function(id) {
          return axios.get(`${archive_paper_prefix}/detail/${id}`)
      },
      search: function(data) {
          return axios.post(`${archive_paper_prefix}/search`, data)
      }  
    },
    album : {
        get: function(page=1) {
            return axios.get(`${archive_album_prefix}/${page}`)
        },
        delete: function(id) {
            return axios.delete(`${archive_album_prefix}/${id}`)
        },
        update: function(data) {
            return axios.patch(`${archive_album_prefix}`, data)
        },
        search: function(data) {
            return axios.post(`${archive_album_prefix}/search`, data)
        }  
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

const sec = {
    image,
    archive
}


export default sec

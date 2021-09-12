import base from './base'
import axios from '@/utils/surf/http'

const sec_prefix = `${base.scout}/sec`

const archive_prefix = `${sec_prefix}/archive`
const archive_paper_prefix = `${archive_prefix}/paper`
const archive_album_prefix = `${archive_prefix}/album`

const archive = {
    paper: {
        get: function(title) {
            return axios.get(`${archive_paper_prefix}/${title}`)
        },
        search: function(data) {
            return axios.post(`${archive_paper_prefix}`, data)
        },
        spell: function(data) {
            return axios.post(`${archive_paper_prefix}/spell`, data)
        }
    },
    album: {
        get: function() {
            return axios.get(`${archive_album_prefix}`)
        },
        papers: function(data) {
            return axios.get(`${archive_album_prefix}/${data.name}/${data.page}`)
        }
    }
}

const sec = {
    archive
}


export default sec

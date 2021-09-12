import DOMPurify from 'dompurify'
const filters = {
    format_time: function(val){
      if (val && val.trim().length > 0) return val.replace(/T/g, ' ')
      else return '无限期搁置'
    },
    pure_content: function(val){
      if (val && val.trim().length > 0) {
          val = DOMPurify.sanitize(val)
          if (val.trim().length === 0) val = 'Malicious text -- filtered by manual'
      }else val = "no text"
      return val
    }
}
export default filters
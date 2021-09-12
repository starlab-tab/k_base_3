export default {
    
    check_input_filled: function(data) {
        for (var x of data) {
            x = x.trim()
            if (x.length <= 0) return false
        }
        return true
    },

    get_current_time: function() {
        let yy = new Date().getFullYear()
        let mm = new Date().getMonth() + 1
        let dd = new Date().getDate()
        let hh = new Date().getHours()
        let mf = new Date().getMinutes()
        let ss = new Date().getSeconds()
        mm = mm + 1 < 10 ? '0' + mm : mm
        dd = dd < 10 ? '0' + dd : dd
        hh = hh < 10 ? '0' + hh : hh
        mf = mf < 10 ? '0' + mf : mf
        ss = ss < 10 ? '0' + ss : ss
    　　return `${yy}-${mm}-${dd} ${hh}:${mf}:${ss}`
    },

    scroll_to_bottom: function(self) {
        self.$nextTick(() => {
            self.$vuetify.goTo(document.body.scrollHeight)
        })
    },

    is_mobile: function() {
        let flag = navigator.userAgent.match(/(phone|pad|pod|iPhone|iPod|ios|iPad|Android|Mobile|BlackBerry|IEMobile|MQQBrowser|JUC|Fennec|wOSBrowser|BrowserNG|WebOS|Symbian|Windows Phone)/i);
        return flag ? true : false
    }

}
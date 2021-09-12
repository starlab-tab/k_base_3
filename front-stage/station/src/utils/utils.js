export default {
    leave_check: function(base, valite) {
        if (Object.keys(base).length != Object.keys(valite).length) {
            return false
        } else {
            for (var key in base) {
                if (valite.hasOwnProperty(key)) {
                    if (Array.isArray(valite[key])) {
                        if (!this.arrayCmp(base[key], valite[key])) return false
                    } else {
                        if (!Object.is(base[key], valite[key])) {
                            return false;
                        }
                    }
                } else {
                    return false
                }
            }
            return true
        }
    },
    
    get_update_map: function(base, valite) {
        let diff_attrs = []
        for (var key in base) {
            if (valite.hasOwnProperty(key)) {
                if (Array.isArray(valite[key])) {
                    if (!this.arrayCmp(base[key], valite[key])) diff_attrs.push(key)
                } else {
                    if (!Object.is(base[key], valite[key])) {
                        diff_attrs.push(key)
                    }
                }
            }
        }
        let data = {}
        for (var i = 0, len = diff_attrs.length; i != len; ++i) {
            data[diff_attrs[i]] = valite[diff_attrs[i]]
        }
        return Object.keys(data).length ? data : undefined
    },
    
    get_crawler_update_map: function(oc, nc, key=undefined) {
        let diff_attrs = []
        if (Object.keys(oc).length != Object.keys(nc).length) {
            if (key) diff_attrs.push(key)
            else return undefined
        } 
        for (var key in nc) {
            if (oc.hasOwnProperty(key)) {
                if (Array.isArray(nc[key])) {
                    if (!this.arrayCmp(oc[key], nc[key])) diff_attrs.push(key)
                } else if (nc[key] instanceof Object) {
                    let new_rules = this.get_crawler_update_map(oc[key], nc[key], key)
                    if (new_rules) diff_attrs.push(key)
                } else {
                    if (!Object.is(oc[key], nc[key])) {
                        diff_attrs.push(key)
                    }
                }
            }else {
                diff_attrs.push(key)
            }
        }
        let data = {}
        for (var i = 0, len = diff_attrs.length; i != len; ++i) {
            data[diff_attrs[i]] = nc[diff_attrs[i]]
        }
        return Object.keys(data).length ? data : undefined
    },
    
    arrayCmp: function(o, n) {
        if (o.length !== n.length) {
            return false
        } else {
            for (let i = 0; i < o.length; i++) {
                if (o.indexOf(n[i]) === -1) {
                    return false
                }
            }
            return true
        }
    },
    
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
// https://www.jianshu.com/p/eb325d70990b?utm_medium=timeline
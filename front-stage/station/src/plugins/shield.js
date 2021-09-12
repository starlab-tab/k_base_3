const shieldPlugin = {
    install: (Vue, {
        store
    }) => {
        if (!store) {
            throw new Error("Please provide vuex store.");
        }
        Vue.prototype.$shield = {
            up: function(msg="Please Stand By...", action=true) {
                store.commit(
                    "shield/show", {
                        msg,
                        action
                    }, {
                        root: true
                    }
                );
            },
            down: function(msg="Please Stand By...", action=false) {
                store.commit(
                    "shield/show", {
                        msg,
                        action
                    }, {
                        root: true
                    }
                );
            },
        };
    }
};
export default shieldPlugin;

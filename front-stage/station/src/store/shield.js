const state = () => ({
    msg: "",
    action: ""
});
const mutations = {
    show(state, payload) {
        state.msg = payload.msg;
        state.action = payload.action;
    }
};
export default {
    namespaced: true,
    state,
    mutations
};

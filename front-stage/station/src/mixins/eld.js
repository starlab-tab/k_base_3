// editor leave dialog
export const eld={
    beforeMount() {
        window.addEventListener("beforeunload", event => {
            if (this.$refs.Editor.check_dessert_state()) return
            event.preventDefault()
            event.returnValue = ""
        })
        sessionStorage.setItem('is_editor_done',false)
    },
    async beforeRouteLeave(to, form, next) {
        if (sessionStorage.getItem('is_editor_done') === 'true') {
            sessionStorage.removeItem('is_editor_done')
            next()
        }else {
            if (this.$refs.Editor.check_dessert_state()) {
                sessionStorage.removeItem('is_editor_done')
                next()
            } else {
                if (
                    await this.$dialog.warning({
                        text: 'confirm to leave ?',
                        title: 'Warning',
                        actions: {
                            false: "No",
                            true: {
                                color: 'primary',
                                text: "OK"
                            }
                        }
                    })
                ) {
                    next()
                }else {
                    next(false)
                }
            }
        }
    },
}
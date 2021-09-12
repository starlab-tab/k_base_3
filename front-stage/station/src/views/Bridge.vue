<template>
    <v-container fill-height fluid justify-center>
        <v-simple-table dark v-if="info">
            <template v-slot:default>
                <thead>
                    <tr>
                        <th class="text-left">
                            IP
                        </th>
                        <th class="text-left">
                            XFF
                        </th>
                        <th class="text-left">
                            AGENT
                        </th>
                        <th class="text-left">
                            COMMENT
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{{ info['X-Real-Ip'] | msg_filter}}</td>
                        <td>{{ info['X-Forwarded-For'] | msg_filter}}</td>
                        <td>{{ info['User-Agent'] | msg_filter}}</td>
                        <td>{{ info['comment'] | msg_filter}}</td>
                    </tr>
                </tbody>
            </template>
        </v-simple-table>
        <v-window v-model="auth_step" reverse class="d-flex flex-column justify-center" v-else>
            <v-window-item>
                <v-text-field v-model="ident" background-color="transparent" autofocus dark hide-details solo flat placeholder="I"
                    @keydown.native.enter="next"></v-text-field>
            </v-window-item>
            <v-window-item>
                <v-text-field 
                    v-model="auth" 
                    :loading="loading" 
                    background-color="transparent" 
                    color="secondary" dark
                    autofocus hide-details solo flat placeholder="A" 
                    @keydown.native.enter="next"
                    :disabled="disabled"
                    type="password"
                >
                </v-text-field>
            </v-window-item>
        </v-window>
    </v-container>
</template>

<script>
    export default {
        data() {
            return {
                ident: "",
                auth: "",
                auth_step: 0,
                loading: false,
                snackbar: false,
                disabled: false,
                info: undefined
            }
        },
        filters: {
            msg_filter: function(val) {
                // var map = {
                //     '&': '&amp;',
                //     '<': '&lt;',
                //     '>': '&gt;',
                //     '"': '&quot;',
                //     "'": '&#039;'
                // }
                // return val.replace(/[&<>"']/g, function(m) { return map[m]; })
                return val
            }
        },
        methods: {
            next: function() {
                if (this.auth_step === 0 && this.ident.trim().length === 0) {
                    this.ident = this.ident.trim()
                    return
                }
                if (this.auth_step === 1 && this.auth.trim().length === 0) {
                    this.auth = this.auth.trim()
                    return
                }
                if (this.ident === 'clear' || this.auth === 'clear') {
                    this.auth = ''
                    this.ident = ''
                    this.auth_step = 0
                    return
                }
                if (!this.auth_step) this.auth_step++
                else {
                    this.loading = true
                    this.submit()
                }
            },
            init: async function() {

            },
            submit: async function() {
                this.disabled = true
                let data = await this.$surf.bridge.init_auth().then(res => {
                    this.loading = false
                    if (res.data.msg) {
                        this.info = res.data.msg
                        this.byebye()
                    }
                    else {
                        return res.data
                    }
                }).catch(err => {
                    this.loading = false
                    this.disabled = false
                })
                if (data && Object.keys(data).length!==0) {
                    this.$surf.bridge.auth({
                        ident: this.fuzz(data.key, this.ident),
                        auth: this.fuzz(data.key, this.auth),
                    }).then(res => {
                        if (res.data.msg) {
                            this.info = res.data.msg.map(x => {
                                return x.replace
                            })
                            this.info = res.data.msg
                            
                            this.byebye()
                            return
                        }
                        this.disabled = false
                        this.loading = false
                        let key = res.data.language
                        let token = res.data.access_token
                        if (key && token) {
                            localStorage.setItem("language", key)
                            localStorage.setItem(key, token)
                            this.$router.replace({
                                name: 'Dashbord'
                            })
                        }else {
                            this.$dialog.notify.error('fail', {
                                position: 'top-right',
                                timeout: 5000
                            })
                        }
                        this.loading = false
                    }).catch(err => {
                        this.loading = false
                        this.disabled = false
                    })
                }
            },
            fuzz: function(key, raw) {
                let publicKey = this.$forge.pki.publicKeyFromPem(this.$forge.util.decode64(key))
                var encrypted = publicKey.encrypt(raw, 'RSA-OAEP', {
                    md: this.$forge.md.sha256.create(),
                    mgf1: {
                        md: this.$forge.md.sha256.create()
                    }
                })
                return this.$forge.util.encode64(encrypted)
            },
            byebye: function() {
                // let window_ = window
                // setTimeout(function() {
                //     window_.location.href = "https://google.com"
                // }, 6000)
            },
            filter_char: function() {
                
            }
        }
    }
</script>

<style lang="scss" scoped>
    ::v-deep {
        .v-window {
            height: 12.5rem;
            width: 22.5rem;

            .v-window__container {
                height: fit-content !important;

                .v-window-item {
                    padding: 1rem;

                    .v-input {
                        input {
                            font-size: 1.125rem;
                            min-height: 3.75rem;
                            max-height: 3.75rem;
                        }
                    }
                }
            }
        }
    }
</style>

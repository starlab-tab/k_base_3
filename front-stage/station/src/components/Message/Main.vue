<template>
    <v-container fluid fill-height align-start justify-center class="pa-0">
        <v-row class="message-board pa-0 pt-3 ma-0">
            <v-col cols="12">
                <v-textarea
                    v-model="message.text"
                    class="msg-input"
                    rows="3"
                    outlined auto-grow hide-details dark
                    label="Please leave a message 請留言 ..."
                >
                    <template #append>
                        <v-text-field
                            v-model="message.texter"
                            outlined hide-details
                            style="z-index: 100;"
                            @keydown.native.enter="new_send"
                        ></v-text-field>
                    </template>
                </v-textarea>
            </v-col>
            <v-progress-linear
                v-show="loading"
                indeterminate
                class="mx-3"
                color="secondary"
                height="3"
            ></v-progress-linear>
            <v-col cols="12">
                <div class="messages">
                    <div v-if="desserts.length > 0">
                        <div class="message"
                            v-for="(dessert, index) in desserts"
                            :key="index"
                        >
                            <div class="top">
                                <span
                                    class="texter font-italic"
                                    :style="{ color: dessert.marked ? '#fbd300' : ''}"
                                    @click="edit(index)"
                                >
                                    From: {{dessert.texter | pure_content}}
                                </span>
                                <p>{{ dessert.text | pure_content}}</p>
                                <div class="text-end">
                                    <span 
                                        class="text-time" 
                                        style="width: inherit;"
                                    >
                                        {{ sv_time(dessert) | format_time }}
                                    </span>
                                </div>
                            </div>
                            <div class="top ml-4 mt-2 supervisor" v-if="dessert.supervisor && dessert.supervisor.length > 0">
                                <span
                                    class="texter font-italic"
                                >
                                    From: Supervisor
                                </span>
                                <p>{{ dessert.supervisor | pure_content}}</p>
                                <div class="text-end"><span class="text-time" style="width: inherit;">{{dessert.updated_at | format_time}}</span></div>
                            </div>
                        </div>
                    </div>

                    <span v-else style="color:#b1b1b1 ">no message</span>
                </div>
            </v-col>
            <v-col cols="12"
                class="pt-0"
                style="position: sticky; bottom: 0;"
            >
                <v-btn
                    v-if="next_page && desserts.length > 0"
                    depressed
                    block
                    style="background: transparent;"
                    @click="get()"
                >
                    <v-icon>{{show_retry ? 'mdi-refresh' : 'mdi-chevron-double-down'}}</v-icon>
                </v-btn>
            </v-col>
        </v-row>
        <v-dialog v-model="show_edit_dlg" max-width="1000px">
            <v-card dark color="primary">
                <v-card-title>
                    <span class="headline" style="color:#fbd300">edit</span>
                </v-card-title>
                <v-card-text class="py-0">
                    <v-textarea
                        v-model="edit_item.text"
                        class="msg-input"
                        rows="3"
                        outlined auto-grow hide-details
                    >
                        <template #append>
                            <v-text-field
                                v-model="edit_item.texter"
                                outlined hide-details
                                label="From"
                                style="z-index: 100;"
                                @keydown.native.enter="send"
                            ></v-text-field>
                        </template>
                    </v-textarea>
                </v-card-text>
                <v-card-text class="py-0" v-if="!edit_item.marked">
                    <v-text-field
                        v-model="edit_item.supervisor"
                        @keydown.native.enter="send"
                        autofocus
                    ></v-text-field>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="grey" class="text-capitalize" icon @click="show_edit_dlg = false">
                        <v-icon>
                            mdi-cancel
                        </v-icon>
                    </v-btn>
                    <v-btn color="red" class="text-capitalize" icon @click="del">
                        <v-icon>
                            mdi-trash-can-outline
                        </v-icon>
                    </v-btn>
                    <v-btn color="green accent-3" class="text-capitalize" icon @click="send">
                        <v-icon>
                            mdi-check-bold
                        </v-icon>
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script>
    import Utils from '@/utils/utils.js'
    import DOMPurify from 'dompurify'
    export default {
        data: () => ({
            next_page: 1,
            message: {
                texter: "Supervisor",
                text: "",
                marked: true
            },
            desserts: [],
            show_retry: false,
            boss_msg: "",
            show_edit_dlg: false,
            edited_index: -1,
            edit_item: {},
            base_item: {},
            loading: false
        }),
        created() {
            this.get()
        },
        methods: {
            get: function() {
                this.loading = true
                this.$surf.main.message.get(this.next_page).then(res => {
                    this.show_retry = false
                    this.desserts.push(...res.data.data)
                    this.next_page = res.data.next_page
                    Utils.scroll_to_bottom(this)
                }).catch(err => {
                    this.show_retry = true
                }).finally(result => {
                    this.loading = false
                })
            },
            new_send: function() {
                this.$shield.up()
                if (!Utils.check_input_filled([this.message.texter, this.message.text])) return
                let data = {texter: this.message.texter, text: this.message.text, marked: this.message.marked}
                this.$surf.main.message.post(data).then(res => {
                    this.message.texter = ""
                    this.message.text = ""
                    this.message.marked = true 
                    data.created_at = Utils.get_current_time()
                    data.id = res.data.id
                    this.desserts.unshift(data)
                }).catch(err => {
                    this.show_retry = true
                }).finally(result => {
                    this.$shield.down()
                })
            },
            send: function() {
                this.$shield.up()
                if (!Utils.check_input_filled([this.edit_item.texter, this.edit_item.text])) return
                let data = Utils.get_update_map(this.base_item, this.edit_item)
                if (!data) return
                data.id = this.edit_item.id
                this.$surf.main.message.patch(data).then(res => {
                    this.edit_item.updated_at = Utils.get_current_time()
                    this.show_edit_dlg = false
                    this.desserts[this.edited_index] = Object.assign({}, this.edit_item)
                    this.$dialog.notify.success('done', {
                        position: 'top-right',
                        timeout: 2000
                    })
                }).catch(err => {
                    console.log(err)
                    this.show_retry = true
                }).finally(result => {
                    this.$shield.down()
                })
            },
            edit: function(index) {
                this.edited_index = index
                this.edit_item = Object.assign({}, this.desserts[index])
                this.base_item = Object.assign({}, this.desserts[index])
                this.show_edit_dlg = true
            },
            del: function() {
                this.$shield.up()
                this.$surf.main.message.delete(this.edit_item.id).then(res => {
                    this.show_edit_dlg = false
                    this.desserts.splice(this.edited_index, 1)
                    this.$dialog.notify.success('done', {
                        position: 'top-right',
                        timeout: 2000
                    })
                    this.show_edit_dlg = false
                }).catch(err => {
                }).finally(result => {
                    this.$shield.down()
                })
            },
            sv_time: function(dessert) {
                let text = dessert.marked ? dessert.updated_at : dessert.created_at
                if (!text) return dessert.created_at
                return text 
            }
        }
    }
</script>

<style lang="scss" scoped>
    .message-board {
        max-width: 60%!important;
        @media only screen and (max-width: 768px) {
            max-width: 100%!important;
        }
        .msg-input {
            ::v-deep {
                .v-input__append-inner {
                    margin: 0;
                    align-self: center;
                }
            }
        }
        .messages {
            color: white;
            padding: 6px 16px;
            border: 2px solid #DBDBDB;
            ::v-deep {
                .message {
                    margin: 16px 0px;
                    .top {
                        border-bottom: 1px solid white;
                        .texter {
                            &:hover {
                                transition: .3s;
                                color: #fbd300;
                                cursor: pointer;
                            }
                            font-weight: 700;
                        }
                    }
                    div:nth-child(2) {
                        .texter {
                            color: #fbd300;
                        }
                    }
                    .text-time {
                        font-size: .8rem;
                    }
                    p {
                        margin: 0;
                    }
                }
            }
        }
    }
</style>

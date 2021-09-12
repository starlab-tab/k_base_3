<template>
    <v-container fluid fill-height align-start justify-center class="pa-0"  style="background-color:#f9f7f1">
        <v-row class="message-board pa-0 pt-3 ma-0">
            <v-col cols="12">
                <v-textarea
                    v-model="text"
                    class="msg-input"
                    rows="3"
                    :loading="loading"
                    outlined auto-grow hide-details
                    label="Please leave a message 請留言 ..."
                >
                    <template #append>
                        <v-text-field
                            v-model="texter"
                            outlined hide-details
                            label="From(tab)"
                            style="z-index: 100;"
                            @keydown.native.enter="send_msg"
                        ></v-text-field>
                    </template>
                </v-textarea>
            </v-col>
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
                                    :style="{ color: dessert.marked ? '#367bf0' : ''}"
                                >
                                    From: {{dessert.texter | pure_content}}
                                </span>
                                <p>{{ dessert.text | pure_content}}</p>
                                <div class="text-end">
                                    <span 
                                        class="text-time" 
                                        style="width: inherit;"
                                    >
                                        {{dessert.marked ? dessert.updated_at : dessert.created_at | format_time}}
                                    </span>
                                </div>
                            </div>
                            <div class="top ml-4 mt-2" v-if="dessert.supervisor && dessert.supervisor.length > 0">
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
                    v-if="next_page"
                    depressed
                    block
                    :loading="loading"
                    :disabled="loading"
                    style="background: transparent;"
                    @click="get()"
                >
                    <v-icon>{{show_retry ? 'mdi-refresh' : 'mdi-chevron-double-down'}}</v-icon>
                </v-btn>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    import Utils from '@/utils/utils.js'
    import DOMPurify from 'dompurify'
    export default {
        data: () => ({
            next_page: 1,
            texter: "",
            text: "",
            desserts: [],
            loading: false,
            show_retry: false,
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
            send_msg: function() {
                if (!Utils.check_input_filled([this.texter, this.text])) return
                this.loading = true
                let data = {texter: this.texter, text: this.text}
                this.$surf.main.message.post(data).then(res => {
                    this.texter = ""
                    this.text = ""
                    data.created_at = Utils.get_current_time()
                    this.desserts.unshift(data)
                }).catch(res => {
                    this.show_retry = true
                }).finally(result => {
                    this.loading = false
                })
            },
        },
        components: {
            MessageText: () => import(`@/components/Global/MessageText.vue`)
        },
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
            padding: 6px 16px;
            border: 2px solid #DBDBDB;
            ::v-deep {
                .message {
                    margin: 16px 0px;
                    div:nth-child(2) {
                        .texter {
                            color: #367bf0;
                        }
                    }
                    .top {
                        border-bottom: 1px solid black;
                    }
                    .texter {
                        font-weight: 700;
                        color: #1E1E1E;
                        cursor: pointer;
                    }
                    .text-time {
                        font-size: .8rem;
                    }
                    p {
                        margin: 0;
                        color: #333;
                    }
                }
            }
        }
    }
</style>

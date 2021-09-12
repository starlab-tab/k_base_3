<template>
    <v-container justify-center fluid class="align-start align-self-start">
        <v-row class="justify-center">
          <v-col cols="12" md="4">
                <v-card dark flat>
                    <v-card-title class="pa-0">
                        <span @click="crawler_expand=!crawler_expand" class="pa-4">Crawler</span>
                        <v-spacer></v-spacer>
                        <div class="pa-3" v-show="crawler_expand">
                            <v-btn color="red" text class="ma-1 text-capitalize" @click="delete_crawler">Del</v-btn>
                            <v-btn color="green" text class="ma-1 text-capitalize" @click="update_crawler">Update</v-btn>
                            <v-btn color="green" text class="ma-1 text-capitalize" @click="create_carwler">Create</v-btn>
                        </div>
                    </v-card-title>
                    <v-expand-transition>
                        <div v-show="crawler_expand">
                            <v-card-text class="py-0">
                                <v-chip-group active-class="blue--text" column v-model="selected_index"
                                    @change="switch_crawler">
                                    <v-chip v-for="item, index in crawlers" :key="index" depressed
                                        active-class="blue--text"
                                        class="ma-1 text-capitalize d-inline-block text-truncate" label
                                        style="max-width: 150px;">
                                        {{ item.platform }}
                                    </v-chip>
                                    <v-btn icon class="ma-1" color="green accent-3" @click="add_crawler">
                                        <v-icon>mdi-plus-circle-outline</v-icon>
                                    </v-btn>
                                </v-chip-group>
                            </v-card-text>
                            <div class="json-editor">
                                <textarea ref="textarea" />
                            </div>
                            <v-card-text class="pa-4 pt-0">
                                <v-text-field v-model="url" flat solo required hide-details solo-inverted class="mt-3"
                                    @keydown.native.enter="active_crawler">
                                    <template v-slot:prepend-inner>
                                        <div class="mr-2 pa-2 blue darken-2 white--text">
                                            URL
                                        </div>
                                    </template>
                                </v-text-field>
                            </v-card-text>
                        </div>
                    </v-expand-transition>
                </v-card>
            </v-col>
            <v-col cols="12" md="8">
               <v-card dark flat>
                    <v-card-title class="pa-0">
                        <span class="pa-4">Previewer</span>
                        <v-spacer></v-spacer>
                        <div class="pa-3">
                            <v-btn color="red" text class="ma-1 text-capitalize" @click="delete_paper">del</v-btn>
                            <v-btn color="green" text class="ma-1 text-capitalize" @click="edit_paper">edit</v-btn>
                        </div>
                    </v-card-title>
                </v-card>
                <v-divider></v-divider>
                <previewer :dessert="paper" style="padding-top: 0!important;"/>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    import CodeMirror from 'codemirror'
    import 'codemirror/addon/lint/lint.css'
    import 'codemirror/lib/codemirror.css'
    import 'codemirror/theme/rubyblue.css'
    require('script-loader!jsonlint')
    import 'codemirror/mode/javascript/javascript'
    import 'codemirror/addon/lint/lint'
    import 'codemirror/addon/lint/json-lint'
    import Utils from '@/utils/utils.js'
    import marked from "marked"
    import DOMPurify from 'dompurify'
    const beautify_html = require('js-beautify').html
    export default {
        data: () => ({
            jsonEditor: false,
            crawler_expand: true,
            selected_index: -1,
            edited_index: -1,
            crawlers: [],
            base_crawler: {
                api: "",
                type: "json",
                base_url: "",
                platform: "",
                pure_tags: [],
                custom: false,
                rules: {
                    author: [],
                    content: [],
                    date: [],
                    title: [],
                },
                url_reg: ""
            },
            url: "",
            paper: {
                content: ""
            },
        }),
        mounted() {
            this.init_crawler()
        },
        components: {
            Previewer: () => import(`@/components/Sec/Archive/Previewer.vue`)
        },
        methods: {
            init_crawler: function() {
                this.$surf.crawler.get().then(res => {
                    if (res.data.data.length <= 0) return
                    this.crawlers = res.data.data
                    this.selected_index = 0
                    this.jsonEditor.setValue(JSON.stringify(this.crawlers[0], null, 4))
                }).catch(err => {})
                this.jsonEditor = CodeMirror.fromTextArea(this.$refs.textarea, {
                    lineNumbers: true,
                    mode: 'application/json',
                    gutters: ['CodeMirror-lint-markers'],
                    theme: 'rubyblue',
                    lint: true
                })
                this.jsonEditor.setValue(JSON.stringify(this.base_crawler, null, 4))
            },
            switch_crawler: function(index) {
                if (typeof(index) === 'undefined') {
                    this.add_crawler()
                    return
                }
                this.selected_index = index
                this.jsonEditor.setValue(JSON.stringify(this.crawlers[index], null, 4))
            },
            add_crawler: function() {
                this.selected_index = -1
                this.jsonEditor.setValue(JSON.stringify(this.base_crawler, null, 4))
            },
            get_valid_crawler: function() {
                try {
                    let obj = JSON.parse(this.jsonEditor.getValue())
                    if (typeof obj == 'object' && obj) {
                        return obj
                    }else {
                        return false
                    }
                } catch (e) {
                    console.log(1)
                    return false
                }
            },
            create_carwler: function() {
                if (this.selected_index !== -1) return
                let valid_crawler = this.get_valid_crawler()
                if (!valid_crawler) return
                this.$shield.up()
                this.$surf.crawler.create(valid_crawler).then(res => {
                    if (res.status === 201) {
                        this.$dialog.notify.success('done', {
                            position: 'top-right',
                            timeout: 2000
                        })
                        valid_crawler.id = res.data.id
                        this.crawlers.push(valid_crawler)
                        this.selected_index = this.crawlers.length - 1
                        this.jsonEditor.setValue(JSON.stringify(valid_crawler, null, 4))
                    }
                }).catch(err => {
                }).finally(result => {
                    this.$shield.down()
                })
            },
            update_crawler: function() {
                if (this.selected_index === -1) return
                let valid_crawler = this.get_valid_crawler()
                if (!valid_crawler) return
                let data = Utils.get_crawler_update_map(this.crawlers[this.selected_index], valid_crawler)
                if (!data)  return
                this.$shield.up()
                data.id = this.crawlers[this.selected_index].id
                data.type = valid_crawler.type
                this.$surf.crawler.update(data).then(res => {
                    this.$dialog.notify.success('done', {
                        position: 'top-right',
                        timeout: 2000
                    })
                    this.crawlers[this.selected_index] = {...valid_crawler}
                }).catch(err => {
                }).finally(result => {
                    this.$shield.down()
                })
            },
            delete_crawler: async function() {
                if (this.selected_index === -1) return
                if (
                    await this.$dialog.warning({
                        text: `Delete Crawler ${this.crawlers[this.selected_index].platform} ?`,
                        title: '',
                    })
                ) {
                    this.$shield.up()
                    this.$surf.crawler.delete(
                        this.crawlers[this.selected_index].id
                    ).then(res => {
                        if (res.status === 204) {
                            this.$dialog.notify.success('done', {
                                position: 'top-right',
                                timeout: 2000
                            })
                            this.crawlers.splice(this.selected_index, 1)
                        }
                        this.selected_index = -1
                        this.jsonEditor.setValue(JSON.stringify(this.base_crawler, null, 4))
                    }).catch(err => {
                    }).finally(result => {
                        this.$shield.down()
                    })
                }
            },
            active_crawler: function() {
                let data = this.als_url()
                if (!data) return
                this.$shield.up()
                this.$surf.crawler.active(data).then(res => {
                    if (res.status === 201 && res.data.data) {
                        this.$dialog.notify.success('done', {
                            position: 'top-right',
                            timeout: 2000
                        })
                        this.paper = res.data.data
                    }else {
                        this.$dialog.notify.error('fail', {
                            position: 'top-bottom',
                            timeout: 2000
                        })
                    }
                }).catch(err => {
                }).finally(result => {
                    this.$shield.down()
                })
            },
            als_url: function() {
                if (this.url.length <= 0) return
                let url_reg = new RegExp(this.crawlers[this.selected_index].url_reg, 'i')
                url_reg = this.url.match(url_reg)
                if (url_reg && url_reg.length === 4) return {
                    platform: this.crawlers[this.selected_index].platform,
                    part_url: url_reg[2],
                    id: url_reg[3]
                }
                else return false
            },
            edit_paper: function() {
                if (!this.paper.id) return
                    this.$router.push({
                        name: 'SecArchiveEdit',
                        params:{
                            id:this.paper.id,
                        },
                    })
            },
            delete_paper: function() {
                if (!this.paper.id) return
                this.$surf.sec.archive.paper.delete(this.paper.id).then(res => {
                    this.paper.id = undefined
                    this.$dialog.notify.success('done', {
                        position: 'top-right',
                        timeout: 2000
                    })
                    this.paper = {content: ""}
                }).catch(err => {})
            },
        }
    }
</script>

<style lang="scss" scoped>
    ::v-deep {
        .previewer {
            height: unset;
        }
        .paper-post {
            width: 100%!important;
            border-radius: unset!important;
        }
    }
    .json-editor {
        height: 100%;
        position: relative;

        ::v-deep {
            .CodeMirror {
                height: auto;
                min-height: 24rem;
                max-height: 37.5rem;
            }

            .CodeMirror-scroll {
                min-height: 24rem;
                max-height: 37.5rem;
            }

            .cm-s-rubyblue span.cm-string {
                color: #F08047;
            }
        }
    }
</style>

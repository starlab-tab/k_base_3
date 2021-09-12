<template>
    <v-container dark class="pa-0 fill-height">
        <editor
            v-model="box"
            ref="Editor"
            @del="del"
            @done="done"
        >
            <template #action>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            v-bind="attrs"
                            v-on="on" 
                            large icon
                            class="text-capitalize ma-1" 
                            @click="box.dessert.render = !box.dessert.render"
                        >
                            <v-icon
                                 :color="box.dessert.render ? 'primary' : ''"
                            >mdi-language-markdown</v-icon>
                        </v-btn>
                    </template>
                    <span>{{box.dessert.render ? 'switch to html' : 'switch to md'}}</span>
                </v-tooltip>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            v-bind="attrs"
                            v-on="on" 
                            color="green" 
                            large icon
                            :disabled="box.dessert.render"
                            class="text-capitalize ma-1" 
                            @click="format_content"
                        >
                            <v-icon>mdi-format-page-break</v-icon>
                        </v-btn>
                    </template>
                    <span>formatter</span>
                </v-tooltip>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            v-bind="attrs"
                            v-on="on" 
                            large icon
                            color="black"
                            class="text-capitalize ma-1" 
                            @click="renderer = !renderer"
                         >
                             <v-icon>mdi-file-compare</v-icon>
                        </v-btn>
                    </template>
                    <span>renderer</span>
                </v-tooltip>
            </template>
            <template #attach>
                <v-col cols="12" md="2" class="pt-0">
                    <v-text-field
                        v-model="box.dessert.author"
                        placeholder="author"
                        :rules="[box.rules.required]"
                        outlined hide-details
                        :color="box.primary"
                    ></v-text-field>
                </v-col>
                <v-col cols="12" md="2" class="pt-0">
                    <v-text-field
                        v-model="box.dessert.pf_id" 
                        placeholder="id"
                        :rules="[box.rules.required]"
                        outlined  hide-details
                        :color="box.primary"
                    ></v-text-field>
                </v-col>
                <v-col cols="12" md="2" class="pt-0">
                    <v-text-field
                        v-model="box.dessert.pf_name"
                        placeholder="name"
                        :rules="[box.rules.required]"
                        outlined  hide-details
                        :color="box.primary"
                    ></v-text-field>
                </v-col>
                <v-col cols="12" md="2" class="pt-0">
                    <v-text-field
                        v-model="box.dessert.date" 
                        placeholder="date"
                        outlined hide-details
                        :color="box.primary"
                    ></v-text-field>
                </v-col>
                <v-col cols="12" md="4" class="pt-0">
                    <v-text-field
                        v-model="box.dessert.pf_url"
                        placeholder="url"
                        :rules="[box.rules.required]"
                        outlined  hide-details
                        :color="box.primary"
                    ></v-text-field>
                </v-col>
            </template>
        </editor>
        <v-dialog
            v-model="renderer"
            width="600px"
        >
            <v-textarea
                v-model="markdown_text"
                placeholder="Markdown"
                flat solo hide-details
                rows="12"
                style="border-radius: 0;"
            >
            </v-textarea>
            <v-divider></v-divider>
            <v-textarea
                v-model="html_text"
                placeholder="Render"
                flat solo hide-details
                rows="16"
                style="border-radius: 0;"
            >
            </v-textarea>
        </v-dialog>
    </v-container>

</template>

<script>
    import { archive_editor } from "@/mixins/sec.js"
    import Utils from '@/utils/utils.js'
    import marked from "marked"
    const beautify_html = require('js-beautify').html
    export default {
        mixins: [archive_editor],
        data: () => ({
            renderer: false,
            markdown_text: "",
            html_text: ""
        }),
        watch: {
            markdown_text: function() {
                this.html_text = this.renderContent()
            }
        },
        methods: {
            del: async function() {
                if (
                    await this.$dialog.warning({
                        text: `Delete Paper ${this.box.dessert.title} ?`,
                        title: '',
                    })
                ) {
                    this.$shield.up()
                    this.$surf.sec.archive.paper.delete(this.id).then(res => {
                        if (res.status === 204) {
                            this.$dialog.notify.success('done', {
                                position: 'top-right',
                                timeout: 2000
                            })
                            this.$router.replace({name: 'SecArchivePaper'})
                        }
                    }).catch(err => {
                    }).finally(result => {
                        this.$shield.down()
                    })
                }
            },
            done: function() {
                let data = Utils.get_update_map(this.box.base_dessert, this.box.dessert)
                if (!data) return
                data.id = this.box.base_dessert.id
                if (this.box.dessert.visible) {
                    delete data.protection
                }else {
                    data.protection = this.box.dessert.protection
                }
                this.box.loading = true
                this.$surf.sec.archive.paper.update(data).then(res => {
                    this.box.base_dessert = {...this.box.dessert}
                    this.$dialog.notify.success('done', {
                        position: 'top-right',
                        timeout: 2000
                    })
                }).catch(err => {
                }).finally(result => {
                    this.box.loading = false
                    this.$shield.down()
                })
            },
            format_content: function() {
                if (!this.box.dessert.render) {
                    console.log(12)
                    this.box.dessert.content = beautify_html(this.box.dessert.content, { 
                            indent_with_tabs: true, 
                            content_unformatted: ['pre', 'code'], 
                            unformatted_content_delimiter: true,
                        }
                    )
                }
            },
            renderContent: function() {
                if (this.markdown_text.length > 0) {
                    let renderer = this.markedRenderer()
                    return marked(this.markdown_text, { renderer })
                }
            },
            markedRenderer: function() {
                const renderer = new marked.Renderer();
                const linkRenderer = renderer.link;
                renderer.link = (href, title, text) => {
                    const localLink = href.startsWith(`${location.protocol}//${location.hostname}`);
                    const html = linkRenderer.call(renderer, href, title, text);
                    return localLink ? html : html.replace(/^<a /,
                        `<a target="_blank" rel="noreferrer noopener nofollow" `);
                }
                return renderer
            },
        },
    }
</script>
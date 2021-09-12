<template>
    <v-container fluid fill-height>
        <div class="paper-post justify-space-between" style="min-height:100%">
            <div>
                <div class="paper-post__heading">
                    <h1 class="post-title">
                        {{ paper.title | pure_content }}
                    </h1>
                    <div class="divider"></div>
                    <v-chip
                        v-for="(album, index) in paper.albums"
                        :key="index"
                        class="mr-2 mt-4 mb-2 text-capitalize"
                        label
                        text-color="SecPrimary"
                        :to="{ name: 'SecArchiveAlbum', params: { name: album } }"
                        style="background-color: #f0f8ff !important; text-transform: capitalize;"
                    >
                        {{ album | pure_content}}
                    </v-chip>
                </div>
                <div class="text-center mt-4">
                    <v-progress-circular
                        v-show="!paper.id"
                        indeterminate
                        color="SecPrimary"
                    ></v-progress-circular>
                </div>
                <article class="paper-post__article" v-html="renderContent"  id='paper-view'/>
            </div>
            <div class="paper-post__footer">
                <div class="chips">
                    <v-chip
                        v-for="(chip, index) in paper.chips"
                        :key="index"
                        class="mr-2 mb-2 text-capitalize"
                        link
                        color="#e8e8e8"
                        text-color="#5a5757"
                    >
                        {{chip | pure_content}}
                    </v-chip>
                </div>
                <v-divider class="my-2"></v-divider>
                <div class="d-flex justify-space-between font-italic" style="color: #9e9e9e;">
                    <div>
                        <span>Author: </span>
                        <span class="text-capitalize font-italic">
                            <a :href="paper.pf_url" target="_blank" rel="noreferrer noopener nofollow"
                                style="color: #367BF0; text-decoration: none;font-weight: 700;">{{paper.author}}</a>
                        </span>
                    </div>
                    <div>
                        <span class="post_date"  style="color: #9e9e9e;">{{paper.date}}</span>
                    </div>
                </div>

                <v-divider class="my-2"></v-divider>
            </div>
        </div>
        <v-dialog 
            transition="dialog-top-transition" 
            persistent max-width="320" 
            v-model="gate" 
            overlay-opacity="0"
        >
            <template v-slot:default="dialog">
                <v-card color="BlogPrimary">
                    <v-card-title
                        style="color: #FFFFFF;"
                    >
                        wave your magic wand and...
                    </v-card-title>
                    <v-text-field
                        v-model="spell"
                        placeholder="Spell"
                        flat solo
                        style="border-radius: 0;"
                        autofocus
                        :disabled="disabled"
                        @keydown.native.enter="check_spell"
                    >
                    </v-text-field>
                </v-card>
            </template>
         </v-dialog>
    </v-container>
</template>


<script>
    import Prism from '@/assets/prismjs/prism.js'
    import '@/assets/prismjs/prism.css'
    import DOMPurify from 'dompurify'
    import Viewer from '@/plugins/viewer.js';
    export default {
        'props': ['name', 'id'],
        data: () => ({
            paper: {
                content: '',
            },
            gate: false,
            spell: "",
            disabled: false,
            num: 1,
        }),
        created() {
            this.get_paper()
        },
        watch: {
            renderContent() {
                this.$nextTick(() => {
                    Prism.highlightAll()
                    const viewer = new Viewer(document.getElementById('paper-view'))
                })
            },
        },
        computed: {
            renderContent: function() {
                if (this.paper.content.trim().length > 0) {
                    if (this.paper.render) {
                        let renderer = this.markedRenderer()
                        return DOMPurify.sanitize(marked(this.paper.content, { renderer }))
                    }else {
                        return DOMPurify.sanitize(this.paper.content)
                    }
                }
            },
        },
        methods: {
            get_paper: function() {
                if (!this.id) return
                if (this.id.length > 40) return
                this.$surf.sec.archive.paper.get(this.id).then(res => {
                    if (res.status === 203) {
                        this.gate = true
                    }else {
                        this.paper = res.data.data
                        document.title = this.paper.title
                    }
                }).catch(err => {
                    this.$router.replace({name: 'SecArchiveAlbum'})
                })
            },
            check_spell: function() {
                this.disabled = true
                this.$surf.sec.archive.paper.spell({pf_id: this.id, spell: this.spell}).then(res => {
                    this.$dialog.notify.success('nice spell', {
                        position: 'top-right',
                        timeout: 2000
                    })
                    this.gate = false
                    this.spell = ""
                    this.paper = res.data.data
                    document.title = this.paper.title
                }).catch(err => {
                    if (err.status === 404) this.limit_spell()
                }).finally(result => {
                    this.disabled = false
                })
            },
            limit_spell: function() {
                if (this.num > 3) {
                    this.$router.replace({name: 'SecArchiveAlbum'})
                }else {
                    this.num++
                }
                this.spell = ""
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
        }
    }
</script>

<style src="@/assets/styles/components/paper-post.scss" scoped lang="scss"></style>

<template>
    <v-container fluid fill-height>
        <div class="blog-post justify-space-between" style="min-height:100%">
            <div>
                <div class="blog-post__heading">
                    <h1 class="post-title">
                        {{ blog_post.title | pure_content}}
                    </h1>
                    <div class="divider"></div>
                    <v-chip
                        v-for="(album, index) in blog_post.albums"
                        :key="index"
                        class="mr-2 mt-4 mb-2"
                        label
                        text-color="BlogPrimary"
                        :to="{name: 'BlogAlbumPost', params: {name: album}}"
                        style="background-color: #f0f8ff !important; text-transform: capitalize;"
                    >
                        {{album}}
                    </v-chip>
                </div>
                <div class="text-center mt-4">
                    <v-progress-circular
                        v-show="!blog_post.id"
                        indeterminate
                        color="BlogPrimary"
                    ></v-progress-circular>
                </div>
                <article class="blog-post__article" v-html="renderContent" id='blog-post-view'/>
            </div>
            <div class="blog-post__footer">
                <div class="chips">
                    <v-chip
                        v-for="(chip, index) in blog_post.chips"
                        :key="index"
                        class="mr-2 mb-2"
                        link
                        color="#e8e8e8"
                        text-color="#5a5757"
                    >
                        {{chip}}
                    </v-chip>
                </div>
                <span class="post_date">{{blog_post.created_at | format_time}} -- Created</span>
                <span class="post_date">{{blog_post.updated_at | format_time}} -- Updated</span>
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
    import marked from "marked"
    import DOMPurify from 'dompurify'
    import Viewer from '@/plugins/viewer.js';
    export default {
        props: ['id'],
        data: () => ({
            blog_post: {},
            gate: false,
            spell: "",
            disabled: false,
            num: 1,
            from: null
        }),
        created() {
            this.get_post()
        },
        watch: {
            renderContent() {
                this.$nextTick(() => {
                    Prism.highlightAll()
                    const viewer = new Viewer(document.getElementById('blog-post-view'))
                })
            }
        },
        computed: {
            renderContent: function() {
                if (this.blog_post.content) {
                    let renderer = this.markedRenderer()
                    return DOMPurify.sanitize(marked(this.blog_post.content, { renderer }))
                }
            },
        },
        methods: {
            get_post: function() {
                if (!this.id) return
                var numReg = /^[0-9]*$/
                var numReg = new RegExp(numReg)
                if (numReg.test(this.id)) {
                    this.$surf.blog.post.detail(this.id).then(res => {
                        if (res.status === 203) {
                            this.gate = true
                        }else {
                            this.blog_post = res.data.data
                            document.title = this.blog_post.title
                        }
                    }).catch(err => {
                        this.back_off()
                    })
                }else {
                    this.back_off()
                }
            },
            check_spell: function() {
                this.disabled = true
                this.$surf.blog.post.spell({id: this.id, spell: this.spell}).then(res => {
                    this.$dialog.notify.success('nice spell', {
                        position: 'top-right',
                        timeout: 2000
                    })
                    this.gate = false
                    this.spell = ""
                    this.blog_post = res.data.data
                    document.title = this.blog_post.title
                }).catch(err => {
                    if (err.status === 404) this.limit_spell()
                }).finally(result => {
                    this.disabled = false
                })
            },
            limit_spell: function() {
                if (this.num > 3) {
                    this.back_off()
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
            back_off: function() {
                let _from = sessionStorage.getItem('referrer')
                if (_from === '/') this.$router.replace({name: 'Blog'})
                else this.$router.replace({path: _from})
            }
        }
    }
</script>

<style src="@/assets/styles/components/blog-post.scss" scoped lang="scss"></style>

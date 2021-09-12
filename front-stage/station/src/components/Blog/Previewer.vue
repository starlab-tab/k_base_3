<template>
    <v-container fluid fill-height>
        <div class="blog-post justify-space-between fill-height">
            <div>
                <div class="blog-post__heading">
                    <h1 class="post-title">
                        {{ dessert.title }}
                    </h1>
                    <div class="divider"></div>
                    <div class="albums">
                        <v-chip 
                            v-for="(album, index) in dessert.albums" 
                            :key="index" 
                            class="mr-2 my-2" 
                            label link 
                            text-color="#367BF0"
                        >
                            {{album}}
                        </v-chip>
                    </div>
                </div>
                <article class="blog-post__article" v-html="renderContent" />
            </div>
            <div class="blog-post__footer">
                <div class="chips">
                    <v-chip v-for="(chip, index) in dessert.chips" :key="index" class="mr-2 mb-2" link color="#e8e8e8"
                        text-color="#5a5757">
                        {{chip}}
                    </v-chip>
                </div>
                <div class="albums"></div>
                <span class="post_date">{{dessert.created_at | format_time}} -- Created</span>
                <span class="post_date">{{dessert.updated_at | format_time}} -- Updated</span>
            </div>
        </div>
    </v-container>
</template>

<script>
    import Prism from '@/assets/prismjs/prism.js'
    import '@/assets/prismjs/prism.css'
    import marked from "marked"
    import DOMPurify from 'dompurify'
    export default {
        "props": {
            dessert: {
                default: {
                    cover: "",
                    title: "",
                    content: "",
                    chips: [],
                    images: [],
                    albums: []
                }
            },
        },
        mounted() {
            Prism.highlightAll()
        },
        data() {
            return {}
        },
        filters: {
            format_time(val) {
                if (val) {
                    return val.replace(/T/g, ' ')
                } else {
                    return '无限期搁置'
                }
            }
        },
        watch: {
            renderContent() {
                this.$nextTick(() => {
                    Prism.highlightAll()
                })
            }
        },
        computed: {
            renderContent: function() {
                if (this.dessert.content.length > 0) {
                    let renderer = this.markedRenderer()
                    return DOMPurify.sanitize(marked(this.dessert.content, { renderer }))
                }
            },
        },
        methods: {
            markedRenderer: function() {
                // https://github.com/markedjs/marked/issues/655
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

<style src="@/assets/styles/components/blog-post.scss" scoped lang="scss"></style>

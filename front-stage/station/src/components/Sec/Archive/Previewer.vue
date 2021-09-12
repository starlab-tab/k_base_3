<template>
    <v-container fluid>
        <div class="paper-post justify-space-between" style="min-height:100%">
            <div>
                <div class="paper-post__heading">
                    <h1 class="post-title">
                        {{ dessert.title }}
                    </h1>
                    <div class="divider"></div>
                    <div class="albums">
                        <v-chip
                            v-for="(album, index) in dessert.albums"
                            :key="index"
                            class="mr-2 mt-4 mb-2"
                            label link
                            text-color="#367BF0"
                        >
                            {{album}}
                        </v-chip>
                    </div>
                </div>
                <article class="paper-post__article" v-html="renderContent"/>
            </div>
            <div class="paper-post__footer">
                <div class="chips">
                    <v-chip
                        v-for="(chip, index) in dessert.chips"
                        :key="index"
                        class="mr-2 mb-2"
                        link
                        color="#e8e8e8"
                        text-color="#5a5757"
                    >
                        {{chip}}
                    </v-chip>
                </div>
                <v-divider class="my-2"></v-divider>
                <div class="d-flex justify-space-between font-italic" style="color: #9e9e9e;">
                    <div>
                        <span>Author: </span>
                        <span class="text-capitalize font-italic">
                            <a :href="dessert.pf_url" target="_blank" rel="noreferrer noopener nofollow"
                                style="color: #367BF0; text-decoration: none;font-weight: 700;">{{dessert.author}}</a>
                        </span>
                    </div>
                    <div>
                        <span class="post_date"  style="color: #9e9e9e;">{{dessert.date}}</span>
                    </div>
                </div>

                <v-divider class="my-2"></v-divider>
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
                    pf_url: 'https://127.0.0.1',
                    author: '',
                    date: '',
                    title: '',
                    content: '',
                    render: false,
                    albums: [],
                    chips: [],
                }
            },
        },
        data: () => ({
        }),
        mounted() {
            Prism.highlightAll()
        },
        watch: {
            'dessert.render': {
                handler(val) {
                    this.dessert.content = this.dessert.content + " "
                    this.dessert.content = this.dessert.content.trim()
                },
                deep: true
            },
            renderContent() {
                this.$nextTick(() => {
                    Prism.highlightAll()
                })
            }
        },
        computed: {
            renderContent: function() {
                if (this.dessert.content.trim().length > 0) {
                    if (this.dessert.render) {
                        return DOMPurify.sanitize(marked(this.dessert.content))
                    }else {
                        return DOMPurify.sanitize(this.dessert.content)
                    }
                }
            },
        },
    }
</script>

<style src="@/assets/styles/components/paper-post.scss" scoped lang="scss"></style>

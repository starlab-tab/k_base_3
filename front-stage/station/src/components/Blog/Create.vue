<template>
    <editor 
        v-model="box"
        ref="Editor"
        @done="done"
        @handle_upload_image="handle_upload_image"
        @als_image="als_image"
    >
    </editor>
</template>

<script>
    import { blog_editor } from "@/mixins/blog.js"
    export default {
        mixins: [blog_editor],
        methods: {
            done: function() {
                if (this.box.dessert.visible) delete this.box.dessert.protection
                this.$surf.blog.post.create(this.box.dessert).then(res => {
                    if (res.status === 201) {
                        this.$dialog.notify.success('done', {
                            position: 'top-right',
                            timeout: 2000
                        })
                        sessionStorage.setItem('is_editor_done',true)
                        this.$router.replace({name: 'BlogPost'})
                    }
                }).catch(err => {
                }).finally(result => {
                    this.$shield.down()
                })
            },
        },
    }
</script>
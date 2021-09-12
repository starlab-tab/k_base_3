<template>
    <div>
        <div class="message" v-for="(dessert, index) in desserts" :key="index">
            <div
                class="top"
            >
                <span
                    class="texter font-italic"
                    @click="action(dessert)"
                >
                    From: {{dessert.texter | pure_content}}
                </span>
                <p>{{ dessert.text | pure_content}}</p>
                <div class="text-end"><span class="text-time" style="width: inherit;">{{dessert.created_at | format_time}}</span></div>
            </div>
            <message-text :desserts="dessert.subs" class="ml-4" @edit="edit" :sub="true"></message-text>
        </div>

    </div>
</template>

<script>
    export default {
        name: "MessageText",
        props: {
            desserts: {
                type: Array,
                default() {
                    return []
                }
            },
            sub: {
                type: Boolean,
                default() {
                    return false
                }
            },
        },
        data: () => ({

        }),
        methods: {
            action: function(item) {
                if (this.sub) this.reply(item)
                else this.edit(item)
            },
            reply: function(item) {
                console.log(this.desserts.indexOf(item))
                // this.$emit('reply', this.desserts.indexOf(item))
            },
            edit: function(item) {
                console.log(this.desserts.indexOf(item))
                this.$emit('edit', this.desserts.indexOf(item))
            }
        }
    }
</script>

<style>
</style>

<template>
    <div>
        <div class="message" v-for="(dessert, index) in desserts" :key="index">
            <span class="texter font-italic">From: {{dessert.texter | pure_content}}</span>
            <p>{{ dessert.text | pure_content}}</p>
            <div class="text-end"><span class="text-time" style="width: inherit;">{{dessert.created_at | format_time}}</span></div>
            <message-text :desserts="dessert.sub"></message-text>
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
            }
        },
        data: () => ({
        }),
    }
</script>

<style>
</style>

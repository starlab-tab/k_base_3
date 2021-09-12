<template>
    <v-container fluid>
        <v-row v-masonry>
            <v-col v-for="(item, index) in items" :key="index" cols="12" md="2" sm="4">
                <v-card tile elevation="0" height="100%">
                    <!-- <v-card-title class="pa-1 text-center">{{item.title}}</v-card-title> -->
                    <v-img contain eager @load="$redrawVueMasonry()" :src="require('@/assets/' + item.img)"></v-img>
                    <v-card-text class="text-center">{{item.title}}</v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>


<script>
    export default {
        data() {
            return {
                items: [{
                        id: 1,
                        title: "sky",
                        img: 'sky.jpg',
                        text: "1231231232312312"
                    },

                    {
                        id: 3,
                        title: "Stranger",
                        img: "Stranger.png"
                    },
                    {
                        id: 4,
                        title: "TooClose",
                        img: "TooClose.jpg"
                    },

                    {
                        id: 5,
                        title: "kimono",
                        img: "kimono.jpg"
                    },
                    {
                        id: 2,
                        title: "wallhaven",
                        img: "wallhaven.jpg"
                    },
                    {
                        id: 6,
                        title: "travelling",
                        img: "travelling.jpg"
                    },
                    {
                        id: 1,
                        title: "sky",
                        img: 'sky.jpg',
                        text: "1231231232312312"
                    },

                    {
                        id: 3,
                        title: "Stranger",
                        img: "Stranger.png"
                    },
                    {
                        id: 4,
                        title: "TooClose",
                        img: "TooClose.jpg"
                    },

                    {
                        id: 5,
                        title: "kimono",
                        img: "kimono.jpg"
                    },
                    {
                        id: 2,
                        title: "wallhaven",
                        img: "wallhaven.jpg"
                    },
                    {
                        id: 6,
                        title: "travelling",
                        img: "travelling.jpg"
                    },
                    {
                        id: 1,
                        title: "sky",
                        img: 'sky.jpg',
                        text: "1231231232312312"
                    },

                    {
                        id: 3,
                        title: "Stranger",
                        img: "Stranger.png"
                    },
                    {
                        id: 4,
                        title: "TooClose",
                        img: "TooClose.jpg"
                    },

                    {
                        id: 5,
                        title: "kimono",
                        img: "kimono.jpg"
                    },
                    {
                        id: 2,
                        title: "wallhaven",
                        img: "wallhaven.jpg"
                    },
                    {
                        id: 6,
                        title: "travelling",
                        img: "travelling.jpg"
                    },
                    {
                        id: 1,
                        title: "sky",
                        img: 'sky.jpg',
                        text: "1231231232312312"
                    },

                    {
                        id: 3,
                        title: "Stranger",
                        img: "Stranger.png"
                    },
                    {
                        id: 4,
                        title: "TooClose",
                        img: "TooClose.jpg"
                    },

                    {
                        id: 5,
                        title: "kimono",
                        img: "kimono.jpg"
                    },
                    {
                        id: 2,
                        title: "wallhaven",
                        img: "wallhaven.jpg"
                    },
                    {
                        id: 6,
                        title: "travelling",
                        img: "travelling.jpg"
                    }
                ],
                tags: [{
                        name: '实战',
                    },
                    {
                        name: 'Web安全',
                    },
                    {
                        name: '靶机练习',
                    },
                    {
                        name: 'vulnhub靶机练习',
                    },
                    {
                        name: '开发环境配置',
                    },
                    {
                        name: '免杀',
                    },
                    {
                        name: 'linux提权',
                    },
                    {
                        name: '信息收集',
                    },
                    {
                        name: '漏洞利用复现',
                    },
                    {
                        name: 'What',
                    },
                ],
            }
        },
        methods: {}
    }
</script>

<style>
</style>
